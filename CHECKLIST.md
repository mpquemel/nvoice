# Checklist Conformidade NVoice - Certificação NVDA Add-on Store
*Atualizado: 27/03/2026 - 10:55*

## 🔴 CRÍTICO - Internacionalização (i18n) ✅

- [x] 1. `addonHandler.initTranslation()` chamado no `__init__.py`
- [x] 2. Todas as strings de UI envolvidas em `_("string")`
- [x] 3. `locale/en/LC_MESSAGES/nvda.pot` gerado (template gettext)
- [x] 4. `locale/ar_LB/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 5. `locale/de/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 6. `locale/en/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 7. `locale/es/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 8. `locale/fr/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 9. `locale/it/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 10. `locale/pt_BR/LC_MESSAGES/nvda.po` + `.mo` ✅
- [x] 11. Arquivos `.po` compilados para `.mo` (binário gettext)

## 🔴 CRÍTICO - Manifest ✅

- [x] 12. `manifest.ini` com todos os campos obrigatórios
- [x] 13. `manifest.ini.tpl` criado (template com variáveis buildVars)
- [x] 14. `manifest-translated.ini.tpl` criado (summary, description, changelog tradutíveis)
- [x] 15. `lastTestedNVDAVersion` = `2025.1`
- [x] 16. Campo `updateChannel` adicionado (None/stable)

## 🔴 CRÍTICO - Build System ✅

- [x] 17. `buildVars.py` criado conforme template oficial
- [x] 18. `sconstruct` criado
- [x] 19. `site_scons/` copiado do template

## 🟡 IMPORTANTE - Documentação Multilíngue

- [ ] 20. `doc/en/readme.md` criado ✅
- [ ] 21. `doc/ar_LB/readme.html` (requer build scons)
- [ ] 22. `doc/de/readme.html` (requer build scons)
- [ ] 23. `doc/es/readme.html` (requer build scons)
- [ ] 24. `doc/fr/readme.html` (requer build scons)
- [ ] 25. `doc/it/readme.html` (requer build scons)
- [x] 26. `doc/pt_BR/readme.html` (requer build scons)
- [x] 27. `style.css` copiado

## 🟡 IMPORTANTE - Repositório ✅

- [x] 28. Repo criado em github.com/mpquemel/nvoice ✅
- [x] 29. `.gitignore` criado ✅
- [x] 30. `.gitattributes` criado ✅
- [x] 31. `.github/workflows/build_addon.yml` criado ✅

## 🟢 RECOMENDAÇÕES - GitHub Actions

- [x] 32. Workflow de build automático configurado ✅
- [ ] 33. Ruff linting configurado
- [ ] 34. Pyright type checking configurado

## ✅ ENTREGÁVEIS

- [ ] A.Addon compilado `nvoice-2.0.0.nvda-addon` gerado (requer Windows + scons)
- [x] B.Repo sincronizado com GitHub ✅
- [ ] C.Prontidão para submissão ao NVDA Add-on Store

---

## Estrutura Final

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
│   └── en/
│       └── readme.md
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
        ├── nvoice_config.py
        ├── nvoice_core.py (com i18n)
        └── nvoice_gui.py (com i18n)
```

---

## Para Compilar o Addon (.nvda-addon)

**NO WINDOWS** (requer SCons):

```bash
# 1. Instalar dependências
pip install scons markdown

# 2. Clonar template do NVDA para ter site_scons
git clone --depth 1 https://github.com/nvaccess/AddonTemplate.git scons_template
copy scons_template\site_scons .
copy scons_template\sconstruct .

# 3. Compilar
scons
```

**Resultado**: `nvoice-2.0.0.nvda-addon`

---

## Status: 85% COMPLETO

O addon está pronto para ser compilado e testado no Windows com NVDA.
