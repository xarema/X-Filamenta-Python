# 🚀 COMMANDES RAPIDES — Test Wizard

**Pour tester rapidement les corrections du wizard**

---

## ⚡ LANCEMENT RAPIDE

### Mode Production (Recommandé)

```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue ; Remove-Item "instance\app.db", "instance\installed.flag" -Force -ErrorAction SilentlyContinue ; .\.venv\Scripts\python.exe run_prod.py
```

**Une seule ligne :** Kill serveurs + Clean DB + Lancer serveur

---

### Mode Développement

```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue ; Remove-Item "instance\app.db", "instance\installed.flag" -Force -ErrorAction SilentlyContinue ; .\.venv\Scripts\python.exe scripts\tests\run_dev_test.py
```

---

## 🔍 VÉRIFICATIONS

### Port 5000 occupé ?
```powershell
netstat -ano | findstr :5000
```

### Processus Python en cours ?
```powershell
Get-Process python.exe
```

### Tuer un processus spécifique
```powershell
taskkill /PID <PID> /F
```

---

## 🌐 URL À TESTER

```
http://127.0.0.1:5000/install/
```

---

## ✅ CHECKLIST RAPIDE

- [ ] Fil d'Ariane sur 2 lignes
- [ ] Aucun bouton dupliqué
- [ ] Toutes traductions affichées
- [ ] Wizard complet fonctionne
- [ ] Page "Done" complète

---

## 📚 DOCUMENTATION

- Rapport complet : `Analysis_reports/2025-12-28_19-00_wizard_corrections_complete.md`
- Synthèse : `SYNTHESE_FINALE_CORRECTIONS_WIZARD.md`
- Guide test : `CORRECTIONS_WIZARD_PRET_POUR_TEST.md`
- Règles projet : `.github/READ_BEFORE_ANY_CHANGE.md`

---

**Tout est prêt ! Lancez la commande et testez ! 🎉**

