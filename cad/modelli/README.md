# Modelli 3D di terzi

I file `.step` stanno qui ma non in git (`.gitignore`): si riscaricano dalle fonti.

| Cartella | File | Fonte | Note |
|---|---|---|---|
| `mg996r/` | `Servo Motor MG996R 3D Model.step`, `Servo MG996R Horn.step` | modello di Dejan Nedelkovski (HowToMechatronics, 2020), copia nel repository GitHub [Matthew-Garcia/SCARA-Robot](https://github.com/Matthew-Garcia/SCARA-Robot/tree/main/3D_Models), scaricata l'8 ottobre 2026 | unità mm, Y verso l'alto; confronto con il datasheet in `docs/dimensioni-componenti.md` |
| `pololu-d42v110fx/` | `d42v110fx.step` | [pololu.com/file/0J2219](https://www.pololu.com/file/0J2219/d42v110fx-step-down-voltage-regulator.step) | regolatore dei servo; stesso ingombro del D24V150Fx |
| `pololu-d24v22fx/` | `d24v22fx.step` | [pololu.com/file/0J1413](https://www.pololu.com/file/0J1413/d24v22fx-step-down-voltage-regulator.step) | regolatore da 5 V della logica |

Per riscaricare il modello del servo con `gh`:

```bash
gh api -H "Accept: application/vnd.github.raw" "repos/Matthew-Garcia/SCARA-Robot/contents/3D_Models/Servo%20Motor%20MG996R%203D%20Model.step" > "cad/modelli/mg996r/Servo Motor MG996R 3D Model.step"
```
