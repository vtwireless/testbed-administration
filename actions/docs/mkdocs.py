import yaml
from textwrap import dedent
from pathlib import Path
p = Path('./playbooks/roles')
docs_folder = Path('./.generated_docs/')
roles = frozenset([d for d in p.iterdir() if d.is_dir()])
for role in roles:
	f = role/'meta'/'main.yml'
	yam = yaml.safe_load(f.read_text())
	docs_folder.mkdir(exist_ok=True)
	deps = frozenset([dep['role'] for dep in yam['dependencies'] if dep['role'] in [role.name for role in roles]])
	deps_string = ''.join([f"- [{dep}]({dep})  \n" for dep in deps])

	md_file = docs_folder/f'{role.name}.md'
	md_file.write_text(f"""
>This was automatically generated using our `mkdocs.py` script using information from the `main.yml` file inside the role's directory  

## Author: {yam['galaxy_info']['author']}  

# Description  
{yam['galaxy_info']['description']}\n  

# Dependencies:
{deps_string if deps_string else 'None'}
""".strip())

vte = Path("./actions/docs/virtual-test-environment.md")

vte_file = docs_folder/'virtual-test-environment.md'
vte_file.write_text(vte.read_text()+'\n- '+'\n- '.join([f"[{role.name.replace('_', ' ').upper()}]({role.name})" for role in roles]))