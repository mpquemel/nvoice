# Checklist Conformidade NVoice - Certificação NVDA Add-on Store
*Atualizado: 27/03/2026*

## 🔴 CRÍTICO - Internacionalização (i18n)

- [ ] 1. `addonHandler.initTranslation()` chamado no `__init__.py`
- [ ] 2. Todas as strings de UI envolvidas em `_("string")`
- [ ] 3. `locale/LC_MESSAGES/nvda.pot` gerado (template gettext - OBS: nome é nvda.po, não nvoice.po!)
- [ ] 4. `locale/ar_LB/LC_MESSAGES/nvda.po` criado e completo
- [ ] 5. `locale/de/LC_MESSAGES/nvda.po` criado e completo
- [ ] 6. `locale/en/LC_MESSAGES/nvda.po` criado e completo (inglês como base)
- [ ] 7. `locale/es/LC_MESSAGES/nvda.po` criado e completo
- [ ] 8. `locale/fr/LC_MESSAGES/nvda.po` criado e completo
- [ ] 9. `locale/it/LC_MESSAGES/nvda.po` criado e completo
- [ ] 10. `locale/pt_BR/LC_MESSAGES/nvda.po` criado e completo
- [ ] 11. Arquivos `.po` compilados para `.mo` (binário gettext)

## 🔴 CRÍTICO - Manifest

- [ ] 12. `manifest.ini` com todos os campos obrigatórios
- [ ] 13. `manifest.ini.tpl` criado (template com variáveis buildVars)
- [ ] 14. `manifest-translated.ini.tpl` criado (summary, description, changelog tradutíveis)
- [ ] 15. `lastTestedNVDAVersion` atualizado para `2025.1`
- [ ] 16. Campo `updateChannel` adicionado

## 🔴 CRÍTICO - Build System

- [ ] 17. `buildVars.py` criado conforme template oficial
- [ ] 18. `sconstruct` criado
- [ ] 19. `site_scons/` copiado do template

## 🟡 IMPORTANTE - Documentação Multilíngue

- [ ] 20. `doc/ar_LB/readme.html` criado
- [ ] 21. `doc/de/readme.html` criado
- [ ] 22. `doc/en/readme.html` criado
- [ ] 23. `doc/es/readme.html` criado
- [ ] 24. `doc/fr/readme.html` criado
- [ ] 25. `doc/it/readme.html` criado
- [ ] 26. `doc/pt_BR/readme.html` atualizado
- [ ] 27. `doc/style.css` copiado

## 🟡 IMPORTANTE - Repositório

- [ ] 28. Repo criado em github.com/mpquemel/nvoice
- [ ] 29. `.gitignore` criado
- [ ] 30. `.gitattributes` criado
- [ ] 31. `.github/workflows/build_addon.yml` criado

## 🟢 RECOMENDAÇÕES - GitHub Actions

- [ ] 32. Workflow de build automático configurado
- [ ] 33. Ruff linting configurado
- [ ] 34. Pyright type checking configurado

## ✅ ENTREGÁVEIS

- [ ] A.Addon compilado `nvoice-x.y.nvda-addon` gerado
- [ ] B.Repo sincronizado com GitHub
- [ ] C.Prontidão para submissão ao NVDA Add-on Store

---

## Estrutura Final Alvo

```
nvoice/
├── LICENSE
├── README.md
├── buildVars.py
├── sconstruct
├── manifest.ini
├── manifest.ini.tpl
├── manifest-translated.ini.tpl
├── .gitignore
├── .gitattributes
├── .github/
│   └── workflows/
│       └── build_addon.yml
├── doc/
│   ├── ar_LB/readme.html
│   ├── de/readme.html
│   ├── en/readme.html
│   ├── es/readme.html
│   ├── fr/readme.html
│   ├── it/readme.html
│   ├── pt_BR/readme.html
│   └── style.css
├── locale/
│   ├── ar_LB/LC_MESSAGES/nvda.po + nvda.mo
│   ├── de/LC_MESSAGES/nvda.po + nvda.mo
│   ├── en/LC_MESSAGES/nvda.po + nvda.mo
│   ├── es/LC_MESSAGES/nvda.po + nvda.mo
│   ├── fr/LC_MESSAGES/nvda.po + nvda.mo
│   ├── it/LC_MESSAGES/nvda.po + nvda.mo
│   └── pt_BR/LC_MESSAGES/nvda.po + nvda.mo
└── globalPlugins/
    └── nvoice/
        ├── __init__.py (com i18n)
        ├── nvoice_config.py (com i18n)
        ├── nvoice_core.py (com i18n)
        └── nvoice_gui.py (com i18n)
```
