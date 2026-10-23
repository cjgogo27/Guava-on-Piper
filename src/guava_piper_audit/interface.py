"""Read-only native/OpenAI tool-call schema audit. Never silently remove arguments."""
import json,re
from collections import Counter
from pathlib import Path

XML_CALL=re.compile(r'<tool_call>\s*(.*?)\s*</tool_call>',re.S)

def calls_in_message(message):
    for item in message.get('tool_calls',[]):
        f=item.get('function',item);args=f.get('arguments',{})
        if isinstance(args,str):args=json.loads(args)
        yield f.get('name'),args
    text=message.get('value',message.get('content',''))
    if isinstance(text,str) and not message.get('tool_calls'):
        for raw in XML_CALL.findall(text):
            obj=json.loads(raw);args=obj.get('arguments',obj.get('parameters',{}))
            if isinstance(args,str):args=json.loads(args)
            yield obj.get('name'),args

def audit_records(records,allowed_properties):
    violations=[];counts=Counter();episodes=Counter()
    for i,record in enumerate(records):
        messages=record.get('messages',record.get('conversations',[]));seen=set()
        for j,message in enumerate(messages):
            role=message.get('role',message.get('from'))
            if role not in ('assistant','gpt'):continue
            for name,args in calls_in_message(message):
                if not isinstance(args,dict):raise ValueError('Tool arguments must be objects')
                if name not in allowed_properties:
                    violations.append({'record':i,'message':j,'tool':name,'reason':'unknown_tool'});continue
                for key in args:
                    if key not in allowed_properties[name]:
                        label=f'{name}.{key}';counts[label]+=1;seen.add(label)
                        violations.append({'record':i,'message':j,'tool':name,'argument':key,'reason':'unsupported_argument'})
        episodes.update(seen)
    return {'records':len(records),'unsupported_call_arguments':dict(counts),
            'affected_records':dict(episodes),'violations':violations,
            'caveat':'Schema incompatibility alone does not establish changed physical behavior or causal performance loss.'}

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('schema',type=Path)
    a=ap.parse_args();text=a.input.read_text(encoding='utf8')
    records=[json.loads(x) for x in text.splitlines() if x.strip()] if a.input.suffix=='.jsonl' else json.loads(text)
    if isinstance(records,dict):records=[records]
    print(json.dumps(audit_records(records,json.loads(a.schema.read_text(encoding='utf8'))),indent=2))

if __name__=='__main__':main()
