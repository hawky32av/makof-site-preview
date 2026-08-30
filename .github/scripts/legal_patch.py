from pathlib import Path
import subprocess

index = Path('index.html')
html = index.read_text(encoding='utf-8')

old_signup = '<div class="signup-form" id="signup-form"><span class="section-kicker">Запись</span><p>Оставьте контактные данные. Я свяжусь с вами и договоримся по времени.</p><iframe'
new_signup = '<div class="signup-form" id="signup-form"><iframe'
if old_signup not in html:
    raise SystemExit('signup block pattern not found')
html = html.replace(old_signup, new_signup, 1)

old_footer = '<footer class="site-footer"><div class="container footer-inner"><span>Дмитрий Маков · ЕГЭ по информатике</span><span>Онлайн</span></div></footer>'
new_footer = '<footer class="site-footer"><div class="container footer-inner"><span>Дмитрий Маков · ЕГЭ по информатике</span><nav class="footer-legal" aria-label="Правовые документы"><a href="privacy.html">Политика обработки ПД</a><a href="consent.html">Согласие на обработку ПД</a></nav><span>Онлайн</span></div></footer>'
if old_footer not in html:
    raise SystemExit('footer pattern not found')
html = html.replace(old_footer, new_footer, 1)
index.write_text(html, encoding='utf-8')

styles = Path('styles.css')
css = styles.read_text(encoding='utf-8')
marker = '/* Legal links and compact signup form. */'
if marker not in css:
    css += '''\n\n/* Legal links and compact signup form. */\n#trial .signup-form > .alfacrm-frame {\n  margin-top: 0;\n}\n.footer-legal {\n  display: flex;\n  flex-wrap: wrap;\n  justify-content: center;\n  gap: 8px 18px;\n}\n.footer-legal a {\n  color: var(--muted);\n  font-size: 13px;\n  text-decoration: underline;\n  text-decoration-color: transparent;\n  text-underline-offset: 3px;\n  transition: color 150ms ease, text-decoration-color 150ms ease;\n}\n.footer-legal a:hover {\n  color: var(--text);\n  text-decoration-color: currentColor;\n}\n@media (max-width: 720px) {\n  .footer-legal {\n    width: 100%;\n    justify-content: flex-start;\n  }\n}\n'''
    styles.write_text(css, encoding='utf-8')

subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=True)
subprocess.run(['git', 'add', 'index.html', 'styles.css'], check=True)
subprocess.run(['git', 'rm', '-f', '.github/scripts/legal_patch.py', '.github/workflows/apply-legal-patch.yml'], check=True)
subprocess.run(['git', 'commit', '-m', 'Add privacy links and simplify signup block'], check=True)
subprocess.run(['git', 'push'], check=True)
