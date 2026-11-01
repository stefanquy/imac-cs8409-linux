# Resterende tests op de iMac — werkende driver behouden

De huidige werkende installatie is snd-hda-codec-cs8409-imac-patched/1.33.1 op kernel 7.0.0-42-generic. Dit plan bestaat uit veilige controles op die installatie en een afzonderlijke, nog niet uitgevoerde integratieproef.

**Op je huidige installatie geen sudo install.sh, sudo uninstall.sh, dkms install/remove, insmod, rmmod of modprobe -r uitvoeren.** Geen kernel verwijderen, geen driverbestanden overschrijven en geen ABI-controle omzeilen. De verwijderaar gebruikt dezelfde pakketnaam/versie als de werkende driver.

## A. Veilige controles op de huidige installatie

Open eerst een gewone terminal in de hoofdmap van deze repository (de map met install.sh). Voer alle stappen in dezelfde terminal uit. Je hoeft hiervoor geen beheerder te worden.

### 1. Maak een privé-testmap en leg de uitgangstoestand vast

```bash
REPO=$(pwd -P)
umask 077
TESTDIR=$(mktemp -d /tmp/imac-audio-test.XXXXXX)
cd "$REPO"
printf 'Privé-testmap: %s\n' "$TESTDIR"
uname -r
cat /sys/class/dmi/id/product_name
dkms status > "$TESTDIR/dkms-before.txt"
cat "$TESTDIR/dkms-before.txt"
MODULE_BEFORE=$(modinfo -n snd_hda_codec_cs8409)
printf '%s\n' "$MODULE_BEFORE" > "$TESTDIR/module-before.txt"
sha256sum "$MODULE_BEFORE" > "$TESTDIR/module-before.sha256"
cat /sys/module/snd_hda_codec_cs8409/srcversion > "$TESTDIR/loaded-before.txt"
cat "$TESTDIR/loaded-before.txt"
```

Verwacht: kernel 7.0.0-42-generic, model iMac18,3, pakket 1.33.1 installed en geladen srcversion 1402FE29928032B7E2AE79F. Het modulepad hoort naar updates/dkms te wijzen. Bij een afwijking eerst onderzoeken; geen correcties installeren. De hashes zijn een vergelijking, geen herstelbare back-up. Er is een afzonderlijke, geteste herstelomgeving nodig voordat je later een echte installatieproef doet.

### 2. Controleer scripts en tests

```bash
bash -n install.sh check-secure-boot.sh uninstall.sh dkms-build.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash install.sh --check
```

Verwacht: syntaxcontrole stil met exitcode 0; zestien tests OK. De derde opdracht herkent nu de exacte unsupported-melding van deze iMac (mokutil-exitcode 255) en eindigt met `Prerequisites OK` en exitcode 0. Dit is uitsluitend een geslaagde vereistencontrole, geen installatietoestemming voor je bestaande driver. Enabled, onbekende meldingen, extra waarschuwingen en afwijkende exitcodes moeten in de tests blijven weigeren. Lokaal compileren vereist geen Secure Boot-inschrijving.

--check bewijst geen ABI-compatibiliteit en controleert nog niet op een bestaande DKMS-registratie/doelmap. De uninstaller heeft geen --check-optie; probeer hem niet met sudo.

### 3. Bouw een aparte bronkopie en controleer ABI

```bash
cp -R "$REPO/codecs" "$REPO/common" "$TESTDIR/"
cp "$REPO/Kbuild" "$REPO/dkms-build.sh" "$REPO/verify-abi.py" "$TESTDIR/"
if bash "$TESTDIR/dkms-build.sh" "$(uname -r)" > "$TESTDIR/build.log" 2>&1
then
    cat "$TESTDIR/build.log"
    printf 'Bouw en gerichte ABI-controle: GESLAAGD\n'
else
    cat "$TESTDIR/build.log"
    printf 'Bouw of ABI-controle MISLUKT; niet installeren of laden.\n'
fi
```

Verwacht: een nieuwe .ko uitsluitend in de privé-testmap; vier PASS-regels voor hda_multi_out, hda_gen_spec, hda_component en hda_component_parent; daarna een gezamenlijke PASS. Alleen compileren maakt geen wijziging in /lib/modules of de geladen driver. Een compilernaamwaarschuwing of overgeslagen BTF-generatie is eerder gezien; de verifier moet ondanks zulke meldingen daadwerkelijk slagen. Bij iedere onbekende of mislukte ABI-uitkomst stoppen met installatieplannen.

Dit controleert vier layouts; het is geen bewijs van volledige ABI- of audiocompatibiliteit. Laad het gebouwde bestand niet om deze proef “af te maken”.

### 4. Controleer de negatieve offline-route

```bash
bash "$TESTDIR/dkms-build.sh" unsupported-offline-test
python3 "$TESTDIR/verify-abi.py" --kver unsupported-offline-test --module "$TESTDIR/snd-hda-codec-cs8409.ko"
```

Beide opdrachten moeten weigeren met exitcode 2. De eerste mag niet gaan compileren; de tweede hoort offline verificatie als niet geïmplementeerd te melden. Geen versievoorwaarde aanpassen om dit groen te krijgen. Hiermee is een weigering getest, geen ondersteuning voor toekomstige kernels.

### 5. Test optioneel het huidige geluid

Deze stap test de al geladen werkende driver, niet de nieuw gebouwde kandidaat. Voer hem zelf uit; de opname blijft privé in TESTDIR en hoort niet in de repository.

Kies in Geluidsinstellingen de interne microfoon en interne luidsprekers. Begin met laag volume. Neem ongeveer vijf seconden spraak op en stop met Ctrl+C:

```bash
pw-record --rate 48000 --channels 2 "$TESTDIR/interne-microfoon.wav"
```

Speel daarna af:

```bash
pw-play "$TESTDIR/interne-microfoon.wav"
```

Noteer verstaanbaarheid, linker/rechter speaker, gekraak en uitval. De 48-kHz aanvraag betreft PipeWire; die kan naar de door de driver ondersteunde hardwarefrequentie omzetten.

Aanvullend, indien je die functies wilt claimen: speel een bekend stil stereo-testbestand af; controleer links/rechts, steek een koptelefoon in en uit en controleer dempen/herstellen van speakers; kies bij een TRRS-headset expliciet de headsetmicrofoon en herhaal de opname. Trek geen microfoonconclusie uit alleen de aanwezigheid van een ALSA-apparaat. Niet uitgevoerde functies blijven “niet getest”. Suspend/resume is een optionele handmatige vervolgproef. Een herstart op de bekende werkende kernel kan pas na stap 6; er is voor deze controle geen nieuwe kernel of driver nodig. Bewaar werk vóór zo’n proef. TESTDIR en de shellvariabelen uit deze sessie kunnen na een herstart verdwenen zijn; bewaar eventueel benodigde metingen eerst in een blijvende privémap en noteer het pad.

### 6. Bewijs dat de installatie onveranderd bleef

```bash
sha256sum -c "$TESTDIR/module-before.sha256"
dkms status > "$TESTDIR/dkms-after.txt"
diff -u "$TESTDIR/dkms-before.txt" "$TESTDIR/dkms-after.txt"
printf '%s\n' "$(modinfo -n snd_hda_codec_cs8409)" > "$TESTDIR/module-after.txt"
diff -u "$TESTDIR/module-before.txt" "$TESTDIR/module-after.txt"
cmp "$TESTDIR/loaded-before.txt" /sys/module/snd_hda_codec_cs8409/srcversion
```

Verwacht: de hashcontrole meldt OK; diff/cmp produceren geen verschillen en eindigen met 0. Bij verschillen eerst onderzoeken. Een gelijk gebleven hash of srcversion is geen zelfstandig bewijs van alle runtime-eigenschappen, maar bevestigt samen met de read-only werkwijze dat deze proeven de geïnstalleerde module/registratie niet vervangen hebben.

## B. Echte installatie/verwijdering: alleen op een aparte testinstallatie

**Nog niet op de huidige productie-installatie uitvoeren.** De specifieke unsupported-firmwaremelding is nu ondersteund en de echte --check slaagt. De vereiste aparte testinstallatie en echte install/remove-proef blijven open. Een geslaagde --check verandert niets aan die scheiding; geen controle uitschakelen.

Gebruik voor de hardwareproef dezelfde iMac, geboot vanaf een aparte Ubuntu-testschijf met een eigen rootbestandssysteem en eigen bootomgeving. De werkende productie-installatie en haar /boot mogen niet gedeeld of schrijfbaar aangekoppeld zijn. Deel evenmin /usr/src, /lib/modules of /var/lib/dkms. Een extra repositorykopie of worktree is geen systeemisolatie. Een VM levert geen iMac-audioproef en voldoet niet aan de hardwarevoorwaarden. Maak de testinstallatie/herstelmogelijkheid eerst concreet; wijzig hiervoor geen productiepartities of bootconfiguratie zonder een apart plan.

Zodra die aparte omgeving bestaat:

1. Boot de eigen testinstallatie op kernel 7.0.0-42-generic. Verifieer met `findmnt /` en `findmnt /boot` welke bestandssystemen je gebruikt, en controleer de volledige mountlijst op gedeelde productiepaden. Boot-/herstelschijf moet bruikbaar zijn. Ga niet verder als de identiteit van de testroot of bootomgeving onzeker is.
2. Controleer `dkms status`, `modinfo -n snd_hda_codec_cs8409` en de afwezigheid van /usr/src/snd-hda-codec-cs8409-imac-patched-1.33.1. Verwacht geen CS8409-DKMS-pakket en een stockmodulepad onder kernel/. Een handmatig geïnstalleerde module onder updates/ is geen schone uitgangstoestand.
3. Leg in een blijvende privémap op de testinstallatie de stockmodulehash, het geselecteerde pad, DKMS-status en de lijst van aanwezige kernels vast, zoals bij A. Gebruik hiervoor bijvoorbeeld `mktemp -d "$HOME/imac-dkms-test.XXXXXX"` na `umask 077`, en noteer het pad voor na een herstart; gebruik hiervoor geen /tmp-map. Gebruik die testbaseline; niet de productiebaseline.
4. Voer op de testinstallatie eerst `bash install.sh --check` en de gewone bronbuild/ABI-controle uit. Alleen een werkelijk geslaagde controle telt; iedere firmwareweigering betekent stoppen.
5. **Uitsluitend op die geïsoleerde testroot:** voer `sudo bash install.sh` uit en bewaar de uitvoer privé. Alle DKMS-fasen moeten slagen. Controleer installed-status, updates/dkms-modulepad en vermagic. De srcversion moet overeenkomen met de zojuist gebouwde kandidaat, maar zegt niet welke module al in het geheugen zit. De installer moet zonder reload/reboot eindigen.
6. Herstart bewust naar diezelfde testinstallatie en dezelfde kernel. Controleer geladen srcversion en herhaal microfoon/speakers/koptelefoonproeven. Pas deze stap kan runtimeclaims over de nieuwe installatie ondersteunen.
7. **Nog steeds uitsluitend op de geïsoleerde testroot:** voer `sudo bash uninstall.sh` uit. Controleer dat alleen dit pakket/versie uit de DKMS-status verdwijnt, het geselecteerde modulepad teruggaat naar de vastgelegde stocklocatie en de stockmodulehash overeenkomt met de testbaseline. Controleer overige kernels/andere DKMS-pakketten op onbedoelde veranderingen. De draaiende module wordt door dit script niet herladen. Bij herstelafwijkingen niet herstarten en geen krachtopties gebruiken.
8. Herstart naar de testinstallatie en controleer de stockmodule opnieuw. Minder werkende audio met de stockdriver is niet hetzelfde als een mislukte verwijdering: de patch kan juist voor de microfoon nodig zijn.
9. De bewaarde /usr/src-bronmap maakt een tweede installatie met het huidige script onmogelijk zonder gecontroleerde opruiming. Test dit alleen op die testroot; herstel bij voorkeur de schone testimage vóór een nieuwe ronde. Niet aan productiebronbestanden komen.
10. Boot terug naar de ongemodificeerde werkende installatie en vergelijk opnieuw haar pad, hash, DKMS-status en geladen bronversie met de productiebaseline.

Een foutinjectie tijdens een echte DKMS-build of een mislukte installatiefase hoort ook uitsluitend op de herstelbare testroot. De huidige zestien tests dekken bouw/verifierfouten en Secure Boot-uitkomsten met tijdelijke afhankelijkheden, maar vervangen geen echte install/remove-proef. Die blijft open totdat de aparte testomgeving beschikbaar is en de volledige proef daar uitgevoerd is.

## Resultaten vastleggen

Noteer per proef PASS / FAIL / NIET UITGEVOERD, datum, model, kernel, kandidaatversie en foutmelding. Rapporteer installatie, ABI-controle en hoorbare werking afzonderlijk. Houd opnamebestanden, volledige systeemlogs en DKMS-signingmateriaal privé. Geen repositorypush is onderdeel van dit plan.
