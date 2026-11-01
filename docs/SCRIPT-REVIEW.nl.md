# Controle installatie- en verwijderingsscripts — 1 november 2026

## Actuele aanvulling — Secure Boot-policy aangepast

De hieronder vastgelegde oorspronkelijke firmwareweigering is opgelost: een succesvolle disabled-melding (exit 0) en uitsluitend de exacte unsupported-melding (exit 255) worden geaccepteerd. Enabled, onbekende/toegevoegde tekst en afwijkende statussen weigeren. De policy staat in check-secure-boot.sh en de installer roept die na de iMac-modelcontrole aan. Zestien tests slagen; de echte install.sh --check slaagt zonder systeemwijzigingen. Geen echte installatie/verwijdering uitgevoerd. De overige bevindingen over bestaande registratie, --all, achterblijvende bronmap en gedeeltelijke fouten blijven gelden.

## Uitkomst van de oorspronkelijke review

De onderzochte scripts bevatten geen aangetroffen route die een mislukte ABI-controle alsnog laat installeren. De pakketnaam en versie zijn vastgelegd, installatie weigert bestaande bronbestanden/CS8409-DKMS-registraties, en de scripts herladen de module niet en herstarten de computer niet.

Dit is geen geslaagde volledige installatie-/verwijderingsproef. Tijdens die oorspronkelijke review werd de installatievoorcontrole geweigerd; verwijderen is onverenigbaar met de opdracht om de werkende driver intact te laten. De scripts waren bij die oorspronkelijke controle niet gewijzigd; de latere Secure Boot-aanpassing is hierboven beschreven.

## Belangrijkste bevindingen

1. **Voer uninstall.sh niet uit op de werkende installatie.** Het roept `dkms remove` aan voor snd-hda-codec-cs8409-imac-patched/1.33.1 met `--all`. Dat is exact het nu geïnstalleerde pakket. De scope is beperkt tot één pakket/versie, maar omvat alle geregistreerde kernels daarvan. Het ontbreken van een live module-unload maakt deze opdracht niet onschadelijk: bestanden en DKMS-registratie worden verwijderd. Het script heeft geen dry-run-optie.
2. **Volledige installatie wordt op de huidige firmware geblokkeerd.** mokutil rapporteert “This system doesn't support Secure Boot” en eindigt niet succesvol. install.sh vereist op een EFI-systeem een succesvolle, exacte disabled-melding. Dat is een veilige weigering, maar ook een functionele beperking voor deze iMac. Een aparte testschijf verandert de firmware niet; de weigering kan daar dus hetzelfde blijven. Voor een volledige installatietest moet de omgang met aantoonbaar niet-ondersteunde Secure Boot eerst afzonderlijk worden opgelost en getest, terwijl enabled/onbekend blijven weigeren. Geen controle overslaan of uitvoer vervalsen.
3. **--check is uitsluitend een vereistencontrole.** Deze route keert terug vóór de controle op bestaande /usr/src-bronnen en DKMS-registraties, bouwt niet en voert de ABI-verifier niet uit. Een geslaagde --check is geen bewijs dat installatie mogelijk of ABI-compatibel is. Op de huidige machine bestaan ook de doelmap én de werkende registratie al; de normale installatieroute zou die weigeren nadat eerdere vereisten zijn geslaagd.
4. **Installatie is niet transactioneel.** De ABI-verifier draait tijdens dkms build vóór dkms install. Bij een latere fout kunnen bronstaging, registratie of een installatie op schijf achterblijven. De afsluitende modulepadcontrole wordt pas na installatie uitgevoerd. Een niet-nul eindcode betekent dus niet altijd dat het hele systeem onaangeraakt bleef. Geen automatische rollback wordt geclaimd.
5. **Herinstalleren na verwijderen is geen ondersteunde eenstapsroute.** uninstall.sh laat de /usr/src-bronmap bewust staan; install.sh weigert een bestaande doelmap. Een tweede installatieronde vereist gecontroleerde opruiming uitsluitend op de testinstallatie, of herstel van een schone testimage. Dit niet oplossen door werkende productiebestanden te verwijderen.
6. **DKMS kan zelf tekenen en sleutels aanmaken.** De wrappers bevatten geen eigen sleutelbeheer, maar DKMS kan standaard tijdens een build lokale certificaten/sleutels maken. Dit is beschreven in de [DKMS 3.2.2-documentatie](https://github.com/dkms-project/dkms/blob/v3.2.2/README.md#module-signing). Kopieer geen volledige /var/lib/dkms-boom naar de repository of een publiek testarchief. De huidige controle heeft geen echte DKMS-build uitgevoerd.

## Uitgevoerde veilige controles tijdens de oorspronkelijke review

- Machine/kernel gelezen: iMac18,3, x86_64, 7.0.0-42-generic; DKMS 3.2.2.
- Alleen pakket 1.33.1 van de gepatchte iMac-driver staat als installed geregistreerd; de module wordt vanaf updates/dkms geselecteerd.
- Geïnstalleerde en geladen module melden beide srcversion 1402FE29928032B7E2AE79F.
- De eerder apart gebouwde kandidaat meldt dezelfde srcversion en de juiste vermagic. Metadata-identiteit is geen afzonderlijke runtimeproef.
- Bash-syntaxcontrole van install.sh, uninstall.sh en dkms-build.sh: geslaagd.
- Alle tien bestaande veiligheidstests: geslaagd. Die controleren onder meer de bouw-/ABI-foutafhandeling, niet de volledige sudo-installatie-/verwijderingsroute.
- install.sh --check: verwachte veilige weigering, exitcode 1, vanwege Secure Boot-status.
- Ongeldige installerparameter: weigering, exitcode 1.
- Ongeldige uninstallerparameter: weigering, exitcode 2.
- Uninstaller zonder rootrechten: weigering, exitcode 1. Er is geen sudo-uninstaller gestart.
- ShellCheck is niet geïnstalleerd; er wordt geen ShellCheck-resultaat geclaimd.
- De lokale DKMS-broncode is gelezen om te bevestigen dat remove ook installed modules verwijdert en dat herstel van originals afhankelijk is van de geregistreerde toestand. “Original modules exist” is op zichzelf geen bewijs dat iedere herstelproef zal slagen.

De geïnstalleerde modulehash, het geselecteerde pad, de geladen srcversion en de DKMS-status zijn vóór en na deze controle vergeleken. Er is geen driver geïnstalleerd, verwijderd, herladen of nieuw geluid opgenomen. Zie [het concrete testplan](IMAC-TESTPLAN.nl.md) voor de vervolgstappen.
