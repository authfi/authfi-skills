"""OKF conformance check for skills/ (OKF spec, section 9), plus what Claude Code needs.

  1. every .md except index.md and log.md has a frontmatter block that parses as YAML
  2. every frontmatter block has a non-empty `type`
  3. index.md has no frontmatter (the root index may carry only okf_version),
     lists every .md beside it, and links to nothing missing
  4. every SKILL.md keeps `name` and `description`, and `name` is its folder

Usage: python scripts/okf_validate.py [bundle-root]   (default: skills)
"""
import io, os, re, sys

RESERVED = {'index.md', 'log.md'}
LINK = re.compile(r'^[*-] \[[^\]]+\]\(([^)]+)\)', re.M)


def frontmatter(text):
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---\n', 4)
    if end < 0:
        return None
    keys = {}
    for line in text[4:end].split('\n'):
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m:
            v = m.group(2).strip()
            # an unquoted value holding ': ' is not YAML: Claude Code reads it, other tools drop the skill
            if ': ' in v and v[0] not in ("'", '"', '[', '{', '>', '|'):
                keys['__unparseable__'] = m.group(1)
            keys[m.group(1)] = v
    return keys


def check(root):
    errs = []
    for d, _, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root).replace('\\', '/')
            text = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')
            fm = frontmatter(text)
            if f == 'index.md':
                if fm is not None and (os.path.abspath(d) != os.path.abspath(root) or set(fm) - {'okf_version'}):
                    errs.append('%s: only the root index.md may have frontmatter, and only okf_version' % rel)
                listed = set(LINK.findall(text))
                for t in listed:
                    if not os.path.exists(os.path.join(d, t)):
                        errs.append('%s: links to missing %s' % (rel, t))
                for g in files:
                    if g.endswith('.md') and g not in RESERVED and g not in listed:
                        errs.append('%s: does not list %s' % (rel, g))
                continue
            if f in RESERVED:
                continue
            if fm is None:
                errs.append('%s: no frontmatter' % rel)
                continue
            if '__unparseable__' in fm:
                errs.append('%s: quote the value of "%s" (it contains ": ")' % (rel, fm['__unparseable__']))
            if not fm.get('type'):
                errs.append('%s: missing type' % rel)
            if f == 'SKILL.md':
                if not (fm.get('name') and fm.get('description')):
                    errs.append('%s: SKILL.md needs name and description' % rel)
                elif fm['name'] != os.path.basename(d):
                    errs.append('%s: name "%s" is not its folder name' % (rel, fm['name']))
    return errs


root = sys.argv[1] if len(sys.argv) > 1 else 'skills'
errors = check(root)
for e in errors:
    print('FAIL  ' + e)
print('%s: %s' % (root, 'conformant' if not errors else '%d error(s)' % len(errors)))
sys.exit(1 if errors else 0)
