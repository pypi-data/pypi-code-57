from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime, timezone, timedelta

from masterdata.models import ApplianceQuality
from masterdata.models import AutonomeActivityStatement
from masterdata.models import BusinessForm
from masterdata.models import Contribution
from masterdata.models import DependentQuality
from masterdata.models import DependentRight
from masterdata.models import Discount
from masterdata.models import FamilyTaxDiscountStatement
from masterdata.models import Legal
from masterdata.models import PauseCategory
from masterdata.models import PayrollMode
from masterdata.models import Pretence
from masterdata.models import PrimeMarriageStatement
from masterdata.models import SimplifiedBurdenSharingContributionTaxLimit
from masterdata.models import RevenueBase
from masterdata.models import RevenueType
from masterdata.models import Tax
from masterdata.models import TimeSheetCategory
from masterdata.models import Title
from masterdata.models import UniformBookingClassificationSystem

from masterdata.models import Pause

from customers.models import Customer
from customers.models import Individual
from customers.models import Organization
from commons.models import Person
from corgy_common.models import gender_male,gender_female, gender_choices
from commons.models import Address
from labor.models import TimeSheet
from labor.models import TimeSheetStatistic
from labor.models import TimeSheetItem

from labor.models import Employment
from labor.models import Salary
from labor.models import BankAccount
from labor.models import Salary
from labor.models import SalaryBlockingItem
from labor.models import Dependence

import calendar
from random import choice, randint
import json

class Command(BaseCommand):
    help = _('Személyre szabott törzsadatok generálása.')

    LOCATIONS = [
        'Budapest',
        'Debrecen',
        'Győr'
        'Kecskemét',
        'Szeged',
        'Washington'
    ]

    STREETS = [
        'Marx Károly',
        'Moszkva',
        'Dob',
        'Szervita'
    ]

    MALE_FIRST_NAMES = [
        'Árpád',
        'Előd',
        'Ond',
        'Kond',
        'Tas',
        'Huba',
        'Töhötöm',
        'Taksony',
        'Zalán',
        'Álmos',
        'Kende',
        'Vajk',
        'Manfréd'
    ]

    ORGANIZATION_NAMES = [
        'Mega',
        'Globál',
        'Hiper',
        'Szuper',
        'Top',
        'Elite',
        'Professional'
    ]

    FEMALE_FIRST_NAMES = [
        'Alexandra',
        'Antónia',
        'Lukrécia',
        'Petúnia',
        'Virág'
    ]

    FAMILY_NAMES = [
        'Zwack',
        'Vad',
        'Kovács',
        'Juhász',
        'Corvin',
        'Bálthy',
        'Kossuth',
    ]

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        TimeSheetItem.objects.all().delete()
        TimeSheet.objects.all().delete()

        BankAccount.objects.all().delete()
        SalaryBlockingItem.objects.all().delete()

        Salary.objects.all().delete()
        Dependence.objects.all().delete()
        Employment.objects.all().delete()

        Organization.objects.all().delete()
        Individual.objects.all().delete()
        Customer.objects.all().delete()
        TimeSheet.objects.all().delete()

        ApplianceQuality.objects.all().delete()
        AutonomeActivityStatement.objects.all().delete()
        BusinessForm.objects.all().delete()
        Contribution.objects.all().delete()
        Tax.objects.all().delete()
        Discount.objects.all().delete()
        DependentQuality.objects.all().delete()
        DependentRight.objects.all().delete()
        FamilyTaxDiscountStatement.objects.all().delete()
        Legal.objects.all().delete()
        PauseCategory.objects.all().delete()
        PayrollMode.objects.all().delete()
        Pretence.objects.all().delete()
        PrimeMarriageStatement.objects.all().delete()
        RevenueBase.objects.all().delete()
        RevenueType.objects.all().delete()
        TimeSheetCategory.objects.all().delete()
        Title.objects.all().delete()
        UniformBookingClassificationSystem.objects.all().delete()

        self.create_appliance_qualities()
        self.create_autonome_activity_statements()
        self.create_business_forms()
        self.create_contributions()
        self.create_dependent_qualities()
        self.create_dependent_rights()
        # TODO: discounts?
        self.create_family_tax_discount_statements()
        self.create_legals()
        self.create_categories_pause()
        self.create_payrollmode()
        self.create_pretences()
        self.create_prime_marriage_statements()
        self.create_revenue_bases()
        self.create_revenue_types()
        self.create_taxes()
        self.create_categories_timesheet()
        self.create_titles()
        self.create_uniform_booking_classification_system()

        self.stdout.write("Adatlapok generálása ... %s" % self.style.SUCCESS("OK"))
        self.generate_persons(firstnames=self.FEMALE_FIRST_NAMES, amount=30)
        self.generate_persons(firstnames=self.MALE_FIRST_NAMES, amount=20)
        self.generate_individuals(amount=15)
        self.generate_organizations(amount=7)
        self.generate_bank_accounts(amount=5)

        self.stdout.write("Adatok generálása ... %s" % self.style.SUCCESS("OK"))
        self.log_pauses()


        self.recruit(headcount=randint(10, 50))
        self.pay_salaries()

    def create_family_tax_discount_statements(self):
        """
        Laki-Studio családi adókedvezmény nyilatkozat törzs generálása
        :return:
        """
        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            FamilyTaxDiscountStatement._meta.verbose_name.title(),
            FamilyTaxDiscountStatement.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_uniform_booking_classification_system(self):
        """
        Laki-Studio FEOR törzs generálása
        :return:
        """
        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            UniformBookingClassificationSystem._meta.verbose_name.title(),
            UniformBookingClassificationSystem.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_autonome_activity_statements(self):
        """
        Laki-Studio önálló tevékenység nyilatkozat törzs generálása
        :return:
        """
        AutonomeActivityStatement.objects.create(code="", name="Nem tett nyilatkozatot")
        AutonomeActivityStatement.objects.create(code="", name="10%-os költséghányad figyelembe vétele")
        AutonomeActivityStatement.objects.create(code="", name="SZJA tv. 3. melléklet II. fejezete szerintibizonylat nélkül elszámolható költség")
        AutonomeActivityStatement.objects.create(code="", name="Nyilatkozat szerinti összeg figyelembe vétele")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            AutonomeActivityStatement._meta.verbose_name.title(),
            AutonomeActivityStatement.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_dependent_qualities(self):
        """
        Laki-Studio eltartott jogosultság törzs generálása
        :return:
        """
        DependentQuality.objects.create(code="0", name="Kedvezménybe nem számítható")
        DependentQuality.objects.create(code="1", name="Kedvezményezett eltartott")
        DependentQuality.objects.create(code="2", name="Eltartott")
        DependentQuality.objects.create(code="3", name="Felváltva gondozott")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            DependentQuality._meta.verbose_name.title(),
            DependentQuality.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_dependent_rights(self):
        """
        Laki-Studio eltartott jogosultság törzs generálása
        :return:
        """
        DependentRight.objects.create(code="0", name="Kedvezménybe nem számítható")
        DependentRight.objects.create(code="4", name="Gyermek után családi pótlékra jogosult vagy ilyen jogosulttal közös háztartásban élő házastárs de családi pótlékra nem jogossult")
        DependentRight.objects.create(code="5", name="Családi pótlékra saját jogán jogosult vagy ilyen jogosulttal közös háztartásban élő hozzátartozó")
        DependentRight.objects.create(code="6", name="Rokkantsági járadékban részesül vagy ilyen személlyel közös háztartásban élő hozzátartozó")
        DependentRight.objects.create(code="7", name="Várandós vagy várandós nő közös háztartásban élő házastársa")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            DependentRight._meta.verbose_name.title(),
            DependentRight.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_appliance_qualities(self):
        """
        Laki-Studio alkalmazás minősége törzs generálása
        :return:
        """
        ApplianceQuality.objects.create(code="20", name="munkaviszony, több munkáltatóval létesített munkaviszony, bedolgozói munkaviszony")
        ApplianceQuality.objects.create(code="71", name="közalkalmazotti jogviszony")
        ApplianceQuality.objects.create(code="72", name="közszolgálati jogviszony")
        ApplianceQuality.objects.create(code="63", name="kormányzati, szolgálati jogviszony")
        ApplianceQuality.objects.create(code="73", name="bírói (ügyészségi) szolgálati jogviszony")
        ApplianceQuality.objects.create(code="70", name="igazságügyi alkalmazotti szolgálati jogviszony")
        ApplianceQuality.objects.create(code="19", name="országgyűlési képviselő, nemzetiségi szószóló")
        ApplianceQuality.objects.create(code="23", name="közfoglalkoztatási jogviszony")
        ApplianceQuality.objects.create(code="80", name="hivatásos nevelőszülői jogvisony")
        ApplianceQuality.objects.create(code="40", name="nevelőszülői foglalkoztatási jogviszony")
        ApplianceQuality.objects.create(code="90", name="fegyveres erők hivatásos vagy szerződéses állományú tagja")
        ApplianceQuality.objects.create(code="88", name="katonai szolgálatot teljesítő önkéntes tartalékos katona")
        ApplianceQuality.objects.create(code="89", name="fegyveres szervek szerződéses állományú tagja")
        ApplianceQuality.objects.create(code="84", name="országgyűlési őrség")
        ApplianceQuality.objects.create(code="62", name="köztársasági elnök házastársa")
        ApplianceQuality.objects.create(code="64", name="állami vezetői szolgálati jogviszony")
        ApplianceQuality.objects.create(code="68", name="prémiumévek programban résztvevő személy")
        ApplianceQuality.objects.create(code="69", name="Különleges foglalkoztatási állományban lévő személy")
        ApplianceQuality.objects.create(code="15", name="szövetkezeti tag,munkaviszony")
        ApplianceQuality.objects.create(code="16", name="szövetkezeti tag vállalkozási vagy megbízási jogviszony")
        ApplianceQuality.objects.create(code="17", name="szociális szövetkezet tagi munkavégzésre irányuló jogviszonyban álló tagja")
        ApplianceQuality.objects.create(code="46", name="tam.szerz.al.szakképző isk.tan.f.tanuló")
        ApplianceQuality.objects.create(code="44", name="ösztöndíjas foglalkoztatás")
        ApplianceQuality.objects.create(code="30", name="kieg.tev.folyt. nem minősülő társas vállalk.")
        ApplianceQuality.objects.create(code="35", name="társas vállalkozó (munkaviszony mellett)")
        ApplianceQuality.objects.create(code="37", name="társas vállalkozó (közép- vagy felsőfokú oktatási intézményben nappali rendszerű oktatás keretében tanulmányokat folytató)")
        ApplianceQuality.objects.create(code="39", name="társas vállalkozó (egyéni vállalkozás mellett)")
        ApplianceQuality.objects.create(code="34", name="társas vállalkozó társas (vállalkozás mellett)")
        ApplianceQuality.objects.create(code="53", name="kiegészítő tevékenységet folytató társas vállalkozó")
        ApplianceQuality.objects.create(code="41", name="megbízási jogviszony,munkavégzésre irányuló egyéb jogviszony")
        ApplianceQuality.objects.create(code="47", name="bedolgozó")
        ApplianceQuality.objects.create(code="65", name="felhasználási szerződésen alapuló megbízási jogviszony")
        ApplianceQuality.objects.create(code="75", name="egyéni vállalkozónak nem minősülő társas vállalkozó")
        ApplianceQuality.objects.create(code="76", name="választott tisztségviselő")
        ApplianceQuality.objects.create(code="77", name="társadalmi megbizatású polgármester")
        ApplianceQuality.objects.create(code="24", name="segítő családtag")
        ApplianceQuality.objects.create(code="91", name="egyházi személy")
        ApplianceQuality.objects.create(code="25", name="adóköteles munkanélküli ellátásban részesülő személy")
        ApplianceQuality.objects.create(code="42", name="adómentes munkanélküli ellátásban részesülő személy")
        ApplianceQuality.objects.create(code="81", name="munka,rehabilitációs díjban/fejlesztési foglalkoztatási díjban részesülő")
        ApplianceQuality.objects.create(code="92", name="gyermeknevelési támogatás")
        ApplianceQuality.objects.create(code="94", name="ápolási díj")
        ApplianceQuality.objects.create(code="83", name="gyermekgondozási díj")
        ApplianceQuality.objects.create(code="93", name="gyermekgondozást segítő ellátás,gyermekgondozási segély")
        ApplianceQuality.objects.create(code="48", name="prémiumévek progr. Résztevevé személy járulék kiegészítés")
        ApplianceQuality.objects.create(code="50", name="mezőgazdasági termelők nyugdíj előtti támogatása")
        ApplianceQuality.objects.create(code="97", name="bizt. Megszűnését követően folyósított csecsemőgondozádi díj,baleseti táppénz, örökbefogadói díj")
        ApplianceQuality.objects.create(code="82", name="más foglalkoztatónál fenálló jogviszonyra tekintettel kifizetett járulékköteles jövedelemben részesülő")
        ApplianceQuality.objects.create(code="59", name="a természetes személy más államban ill.EU/EGT tagállamban biztosított, erről igazolással rendelkezik")
        ApplianceQuality.objects.create(code="100", name="állami szolgálati jogviszony")
        ApplianceQuality.objects.create(code="101", name="állami projektértékelői jogviszony")
        ApplianceQuality.objects.create(code="104", name="rendvédelmi egészségkárosodási kereset kiegészítés, honvédelmi egészségkárosodásikeresetkiegészítés")
        ApplianceQuality.objects.create(code="105", name="rendvédelmi egészségkárosodási járadék, honvédelmi egészségkárosodási járulék")
        ApplianceQuality.objects.create(code="172", name="köztisztviselő, közszolgálati ügykezelő")
        ApplianceQuality.objects.create(code="174", name="Főállású polgármesteri foglalkoztatási jogviszony")
        ApplianceQuality.objects.create(code="173", name="rendelkezési állományban álló bíró vagy ügyész")
        ApplianceQuality.objects.create(code="190", name="független rendészeti panasztestület tagja")
        ApplianceQuality.objects.create(code="106", name="vendégoktató,külügyi szakmai ösztöndíjas jogviszony")
        ApplianceQuality.objects.create(code="107", name="más szervhez vezényelt. Egészségügyi szabadságra jogosult biztosított")
        ApplianceQuality.objects.create(code="108", name="politikai szolgálati jogviszony")
        ApplianceQuality.objects.create(code="109", name="biztosi jogviszony")
        ApplianceQuality.objects.create(code="110", name="honvédelmi alkalmazotti jogviszony")
        ApplianceQuality.objects.create(code="111", name="rendvédelmi igazgatási, szolgálati jogviszony")
        ApplianceQuality.objects.create(code="112", name="gyermekek otthongondozási díja")
        ApplianceQuality.objects.create(code="113", name="hallgatói munkaszerződéssel létrejött munkaviszony")
        ApplianceQuality.objects.create(code="114", name="örökbefogadói díj")
        ApplianceQuality.objects.create(code="115", name="katonai szolgálatot teljesítő önkéntes tartalékos katona")
        ApplianceQuality.objects.create(code="900", name="a tbj.szerint biztosítottnak nem minősülő természetes személy")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            ApplianceQuality._meta.verbose_name.title(),
            ApplianceQuality.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_payrollmode(self):
        """
        Laki-Studio önálló tevékenység nyilatkozat törzs generálása
        :return:
        """
        PayrollMode.objects.create(code="", name="Havibér normál munkarend")
        PayrollMode.objects.create(code="", name="Havibér egyenlőtlen munkarend (munkaidőkeret)")
        PayrollMode.objects.create(code="", name="Órabér")
        PayrollMode.objects.create(code="", name="Időbér alapján")
        PayrollMode.objects.create(code="", name="Távolléti díj alapján")
        PayrollMode.objects.create(code="", name="174-es osztó alapján")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            PayrollMode._meta.verbose_name.title(),
            PayrollMode.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_prime_marriage_statements(self):
        """
        Laki-Studio első házasok nyilatkozat törzs generálása
        :return:
        """
        PrimeMarriageStatement.objects.create(code="", name="Nem vesz igénybe családi kedvezményt")
        PrimeMarriageStatement.objects.create(code="", name="Megosztás nélkül veszi igénybe a családi kedvezményt")
        PrimeMarriageStatement.objects.create(code="", name="Megosztással veszi igénybe a családi kedvezményt")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            PrimeMarriageStatement._meta.verbose_name.title(),
            PrimeMarriageStatement.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_titles(self):
        """
        Laki-Studio előtag törzs generálása
        :return:
        """
        Title.objects.create(code="dr",name="Dr.")
        Title.objects.create(code="drdr",name="Dr. Dr.")
        Title.objects.create(code="drpr",name="Dr. Pr.")
        Title.objects.create(code="id",name="Id.")
        Title.objects.create(code="iddr",name="Id. Dr.")
        Title.objects.create(code="ifj",name="Ifj.")
        Title.objects.create(code="ifjdr",name="Ifj. Dr.")
        Title.objects.create(code="ozv",name="Özv.")
        Title.objects.create(code="ozvdr",name="Özv. Dr.")
        Title.objects.create(code="prdr",name="Pr. Dr.")
        Title.objects.create(code="prof",name="Prof.")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            Title._meta.verbose_name.title(),
            Title.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_business_forms(self):
        """
        Laki-Studio cégformák törzs generálása
        :return:
        """
        BusinessForm.objects.create(code="01", name="Európai szövetkezet")
        BusinessForm.objects.create(code="02", name="Külföldi székhelyű európai gazdasági egyesülés magyarországi telephelye")
        BusinessForm.objects.create(code="03", name="Közjegyzői iroda")
        BusinessForm.objects.create(code="04", name="Európai részvénytársaság")
        BusinessForm.objects.create(code="05", name="Európai gazdasági egyesülés")
        BusinessForm.objects.create(code="06", name="Végrehajtói iroda")
        BusinessForm.objects.create(code="07", name="Külföldi vállalkozás magyarországi fióktelepe")
        BusinessForm.objects.create(code="08", name="Vízgazdálkodási társulat")
        BusinessForm.objects.create(code="09", name="Erdőbirtokossági társulat")
        BusinessForm.objects.create(code="10", name="Közhasznú társaság")
        BusinessForm.objects.create(code="11", name="Oktatói munkaközösség")
        BusinessForm.objects.create(code="12", name="Külföldiek magyarországi közvetlen kereskedelmi képviselete")
        BusinessForm.objects.create(code="13", name="Egyéni cég")
        BusinessForm.objects.create(code="14", name="Részvénytársaság")
        BusinessForm.objects.create(code="15", name="Korlátolt felelősségű társaság")
        BusinessForm.objects.create(code="16", name="Közös vállalat")
        BusinessForm.objects.create(code="17", name="Egyesülés")
        BusinessForm.objects.create(code="18", name="Betéti társaság")
        BusinessForm.objects.create(code="19", name="Jogi személy felelősségvállalásával működő gazdasági munkaközösség")
        BusinessForm.objects.create(code="20", name="Gazdasági munkaközösség")
        BusinessForm.objects.create(code="21", name="Közkereseti társaság")
        BusinessForm.objects.create(code="22", name="Szövetkezet")
        BusinessForm.objects.create(code="23", name="Vállalat")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            BusinessForm._meta.verbose_name.title(),
            BusinessForm.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_contributions(self):
        """
        Laki-Studio járulék törzs generálása
        :return:
        """
        Contribution.objects.create(
            code="ebpm",
            name="NAV Egészségbiztosítási és munkaerő-piaci járulék magánszemélyt, őstermelőt, egyéni vállalkozót, kifizetőt terhelő kötelezettség"
        )
        Contribution.objects.create(
            code="nyba",
            name="NAV Nyugdíjbiztosítási Alapot megillető bevételek magánszemélyt, őstermelőt, egyéni vállalkozót, kifizetőt terhelő kötelezettség"
        )
        Contribution.objects.create(
            code="szja",
            name="NAV Személyi jövedelemadó magánszemélyt, őstermelőt, egyéni vállalkozót, kifizetőt terhelő kötelezettség"
        )
        Contribution.objects.create(
            code="szhja",
            name="NAV Szociális hozzájárulási adó"
        )

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            Contribution._meta.verbose_name.title(),
            Contribution.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_categories_timesheet(self):
        """
        Laki-Studio jelenléti blokk törzs generálása
        :return:
        """
        TimeSheetCategory.objects.create(code="X", name="Ledolgozott napok")
        TimeSheetCategory.objects.create(code="F", name="Fizetett ünnep / Munkaszüneti nap")
        TimeSheetCategory.objects.create(code="I", name="Fizetett igazolt távollét")
        TimeSheetCategory.objects.create(code="S", name="Fizetett szabadság")
        TimeSheetCategory.objects.create(code="G", name="Gyermekek utáni szabadság")
        TimeSheetCategory.objects.create(code="T", name="Tanulmányi szabadság")
        TimeSheetCategory.objects.create(code="E", name="Egyéb rendkivüli szabadság")
        TimeSheetCategory.objects.create(code="B", name="Betegszabadság")
        TimeSheetCategory.objects.create(code="M", name="Pihenőnap")
        TimeSheetCategory.objects.create(code="K", name="Biztosítás szünetelése")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            TimeSheetCategory._meta.verbose_name.title(),
            TimeSheetCategory.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_categories_pause(self):
        """
        Laki-Studió biztosítási törzsadatok generálása.
        :return:
        """
        PauseCategory.objects.create(code="11",name="táppénz")
        PauseCategory.objects.create(code="12",name="baleseti táppénz")
        PauseCategory.objects.create(code="21",name="csecsemőgondozási díj")
        PauseCategory.objects.create(code="22",name="gyermekgondozási díj")
        PauseCategory.objects.create(code="23",name="gyermekgondolást segítő ellátás,gyermekgondozási segély")
        PauseCategory.objects.create(code="41",name="(előzetes) letartoztatás")
        PauseCategory.objects.create(code="42",name="szabadságvesztés")
        PauseCategory.objects.create(code="73",name="igazolatlan távollét")
        PauseCategory.objects.create(code="30",name="katonai szolgálatot teljesítő önkéntes tartalékos katona")
        PauseCategory.objects.create(code="84",name="munkavégzési (szolg.telj) kötelezettség alóli mentesítés, (munkabér, illetmény,táppénz ill.távolléti díj fizetése nélkül)")
        PauseCategory.objects.create(code="51",name="ügyvéd tevékenysége, szabadalmi ügyvivő,közjegyző kamara tagsága,szociális szöv.tagsága szünetel")
        PauseCategory.objects.create(code="52",name="állat- egészségügyi szolgáltató tevékenységet végző állatorvos tevékenysége szünetel")
        PauseCategory.objects.create(code="53",name="tanulószerződés szüneteltetése")
        PauseCategory.objects.create(code="71",name="fizetésnélküli szabadság")
        PauseCategory.objects.create(code="24",name="gyermeknevelési támogatás")
        PauseCategory.objects.create(code="25",name="ápolási díj")
        PauseCategory.objects.create(code="72",name="igazolt távollét")
        PauseCategory.objects.create(code="75",name="jogszerű sztrájk időtartama")
        PauseCategory.objects.create(code="76",name="gyermekek otthongondozási díja")
        PauseCategory.objects.create(code="77",name="örökbefogadói díj")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            PauseCategory._meta.verbose_name.title(),
            PauseCategory.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_taxes(self):
        """
        Laki-Studio adónemek törzs generálása.
        :return:
        """

        Tax.objects.create(code="", name="Rehabilitációs hozzájárulás")

        Tax.objects.create(code="", name="Cégautóadó")

        szja = Tax.objects.create(code="", name="Személyi jövedelemadó")
        Discount.objects.create(tax=szja, name="Négy vagy több gyermeket nevelők kedvezménye")
        Discount.objects.create(tax=szja, name="Családi kedvezmény")
        Discount.objects.create(tax=szja, name="Első házasok kedvezménye")
        Discount.objects.create(tax=szja, name="Személyi kedvezmény")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            Tax._meta.verbose_name.title(),
            Tax.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_legals(self):
        """
        Laki-Studio saját jogviszony törzs generálása.
        :return:
        """
        Legal.objects.create(code="", name="Normál alkalmazott")
        Legal.objects.create(code="", name="Nyugdíjas alkalmazott")
        Legal.objects.create(code="", name="Főfoglalkozású társas vállalkozó (munkaviszonyos)")
        Legal.objects.create(code="", name="Főfoglalkozású társas vállalkozó (megbízásos)")
        Legal.objects.create(code="", name="Társas vállalkozó (társas vállalkozás mellett)")
        Legal.objects.create(code="", name="Társas vállalkozó (munkaviszony mellett)")
        Legal.objects.create(code="", name="Társas vállalkozó (nappali tagozatos tanulmányok mellett)")
        Legal.objects.create(code="", name="Társas vállalkozó (egyéni vállalkozás mellett)")
        Legal.objects.create(code="", name="Nyugdíjas társas vállalkozó")
        Legal.objects.create(code="", name="Választott tisztségviselő")
        Legal.objects.create(code="", name="Megbízási díj")
        Legal.objects.create(code="", name="Ingatlan bérbeadás")
        Legal.objects.create(code="", name="Főfoglalkozási egyéni vállalkozó")
        Legal.objects.create(code="", name="Egyéni vállalkozó (munkaviszony mellett)")
        Legal.objects.create(code="", name="Egyéni vállalkozó (nappali tagozatos tanulmányok mellett)")
        Legal.objects.create(code="", name="Egyéni vállalkozó (társas vállalkozás mellett)")
        Legal.objects.create(code="", name="Nyugdíjas egyéni vállalkozó")
        Legal.objects.create(code="", name="EKHO-s jogviszony (munkaviszonyos)")
        Legal.objects.create(code="", name="EKHO-s jogviszony (nyugdíjas)")
        Legal.objects.create(code="", name="EKHO-s jogviszony (megbízásos)")
        Legal.objects.create(code="", name="Egyszerűsített foglalkoztatás")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            Legal._meta.verbose_name.title(),
            Legal.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_pretences(self):
        """
        Laki-Studio saját jogcím törzs generálása.

        :return:
        """
        Pretence.objects.create(code="AL", name="Állásidő")
        Pretence.objects.create(code="LM", name="Munkabér")
        Pretence.objects.create(code="BS", name="Betegszabadság")
        Pretence.objects.create(code="FS", name="Fizetett szabadság")
        Pretence.objects.create(code="FT", name="Fizetett igazolt távollét")
        Pretence.objects.create(code="FU", name="Fizetett ünnep")
        Pretence.objects.create(code="MF", name="Munkaidőkeret feletti óra")
        Pretence.objects.create(code="MP", name="Munkaidőkeret feletti pótlék 50%")
        Pretence.objects.create(code="P1", name="Bérpótlék 15%")
        Pretence.objects.create(code="P2", name="Bérpótlék 30%")
        Pretence.objects.create(code="P3", name="Bérpótlék 50%")
        Pretence.objects.create(code="P4", name="Bérpótlék 100%")
        Pretence.objects.create(code="P5", name="Készenléti pótlék 20%")
        Pretence.objects.create(code="P6", name="Ügyeleti pótlék 40%")
        Pretence.objects.create(code="T1", name="Rendkivüli m.idő pótlék 50%")
        Pretence.objects.create(code="T2", name="Rendkivüli m.idő pótlék 100%")
        Pretence.objects.create(code="TA", name="Rendkivüli munkaidő díjazása")
        Pretence.objects.create(code="SV", name="Szabadságmegváltás")
        Pretence.objects.create(code="JU", name="Jutalom")
        Pretence.objects.create(code="PR", name="Prémium")
        Pretence.objects.create(code="VK", name="Végkielégítés")
        Pretence.objects.create(code="IB", name="Ingatlan bérbeadás")
        Pretence.objects.create(code="MD", name="Megbízási díj")
        Pretence.objects.create(code="TJ", name="Tagi jövedelem")
        Pretence.objects.create(code="TD", name="Tiszteletdíj")
        Pretence.objects.create(code="EV", name="Egyéni vállalkozói kivét")
        Pretence.objects.create(code="HB", name="Helyi utazási bérlet")
        Pretence.objects.create(code="ME", name="Meleg étkezési utalvány")
        Pretence.objects.create(code="UT", name="Utazási költség")
        Pretence.objects.create(code="S1", name="Szép kártya vendéglátás")
        Pretence.objects.create(code="S2", name="Szép kártya szállás")
        Pretence.objects.create(code="S3", name="Szép kártya szabadidő")
        Pretence.objects.create(code="S4", name="Szép kártya vendéglátás határ felett")
        Pretence.objects.create(code="S5", name="Szép kártya szállás határ felett")
        Pretence.objects.create(code="S6", name="Szép kártya szabadidő határ felett")
        Pretence.objects.create(code="BI", name="Bírósági letiltás")
        Pretence.objects.create(code="GY", name="Gyermektartás")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            Pretence._meta.verbose_name.title(),
            Pretence.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def generate_simplified_burden_sharing_contribution_tax_limits(self):
        """
        Laki-Studio EKHO adózási limit törzs generálása
        :return:
        """
        SimplifiedBurdenSharingContributionTaxLimit.objects.create(code="", name="Meghatározott feor és nyugdíjas magánszemély - 60M")
        SimplifiedBurdenSharingContributionTaxLimit.objects.create(code="", name="Sportszervezet edzője - 250M")
        SimplifiedBurdenSharingContributionTaxLimit.objects.create(code="", name="Hivatásos sportoló - 500M")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            SimplifiedBurdenSharingContributionTaxLimit._meta.verbose_name.title(),
            SimplifiedBurdenSharingContributionTaxLimit.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_revenue_types(self):
        """
        Laki-Studio jövedelem típusa törzs generálása
        :return:
        """
        RevenueType.objects.create(code="", name="Munkaviszonyból származó bérjövedelem")
        RevenueType.objects.create(code="", name="Munkaviszonnyal kapcsolatos költségtérítés")
        RevenueType.objects.create(code="", name="Külszolgálatért kapott jövedelem")
        RevenueType.objects.create(code="", name="Más bérjövedelem")
        RevenueType.objects.create(code="", name="Más, nem önálló tevékenységből származó jövedelmek")
        RevenueType.objects.create(code="", name="Nem önálló tevékenységgel kapcsolatos költségtérítés")
        RevenueType.objects.create(code="", name="Önálló tevékenységre tekintettel kifizetett összeg")
        RevenueType.objects.create(code="", name="Egyéb jövedelem")
        RevenueType.objects.create(code="", name="Egyéni vállalkozói kivét")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            RevenueType._meta.verbose_name.title(),
            RevenueType.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def generate_revenue_bases(self):
        """
        Laki-Studio jövedelem alapja törzs generálása
        :return:
        """
        RevenueBase.objects.create(code="", name="Egyösszegű kifizetés")
        RevenueBase.objects.create(code="", name="Óra/nap")
        RevenueBase.objects.create(code="", name="Óra")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            RevenueBase._meta.verbose_name.title(),
            RevenueBase.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def create_revenue_bases(self):
        """
        Laki-Studio családi adókedvezmény nyilatkozat törzs generálása
        :return:
        """
        FamilyTaxDiscountStatement.objects.create(code="", name="Nem vesz igénybe családi kedvezményt")
        FamilyTaxDiscountStatement.objects.create(code="", name="Megosztás nélkül veszi igénybe a családi kedvezményt")
        FamilyTaxDiscountStatement.objects.create(code="", name="Megosztással veszi igénybe a családi kedvezményt")

        self.stdout.write('Setup: %s törzs (%s record) ... %s' % (
            FamilyTaxDiscountStatement._meta.verbose_name.title(),
            FamilyTaxDiscountStatement.objects.count(),
            self.style.SUCCESS("OK")
        ))

    def generate_bank_accounts(self, amount=10):
        for index in range(0, amount):
            BankAccount.objects.create(
                beneficiary='{name} Bank'.format(name=choice(self.FAMILY_NAMES)),
                account_number='{first}-{second}-{third}'.format(
                    first=randint(10000000, 99999999),
                    second=randint(10000000, 99999999),
                    third=randint(10000000, 99999999),
                ),
            )

    def generate_persons(self, firstnames=[], gender=gender_female, amount=10):

        for index in range(0, amount):
            year = randint(1920, 2020)
            month = randint(1, 12)
            day = randint(*calendar.monthrange(year, month)) % 27 + 1
            city = choice(self.LOCATIONS)
            street = choice(self.STREETS)
            street_number = randint(1, 200)

            self.stdout.write('Generate new person {data} ...'.format(
                data = self.style.WARNING(json.dumps(dict(
                    birth_year = year,
                    birth_month = month,
                    birth_day = day,
                    birt_city = city,
                    birt_street = street,
                    birt_street_number = street_number,
                )))
            ))

            address = Address(raw='{street} utca {street_number}, {city}, Hungary'.format(
                city=city,
                street=street,
                street_number=street_number,
            ))
            address.save()

            Person.objects.get_or_create(
                first_name=choice(firstnames),
                last_name=choice(self.FAMILY_NAMES),
                gender=gender_female,
                birthdate=datetime(year=year, month=month, day=day),
                birthplace=choice(self.LOCATIONS),
                name_of_mother="{last} {first}".format(
                    last=choice(self.FAMILY_NAMES),
                    first=choice(self.FEMALE_FIRST_NAMES)
                ),
                permanent_address=address,
                nationality='hu',
                inland_resident=True,
                tax_number='8{p26}{p79}{p0}'.format(
                    p26=(datetime(year=year,month=month,day=day)-datetime(year=1867,month=1,day=1)).days,
                    p79=randint(100, 999),
                    p0=randint(1, 9),
                ),

            )

    def generate_organizations(self, amount=15):
        """
        Példa társas vállakozások generálása
        :return:
        """
        for index in range(0, amount):
            bf = choice(BusinessForm.objects.all())
            Organization.objects.create_organization(
                name='{a}-{b} Kft.'.format(
                    a=choice(self.ORGANIZATION_NAMES),
                    b=choice(self.ORGANIZATION_NAMES),
                ),
                manager=choice(Person.objects.all()),
                registration_number='{bs}-{cf}-{nnnnnn}'.format(
                    bs=randint(10, 50),
                    cf=str(randint(1, 23)),
                    nnnnnn=randint(100000, 999999)
                ),
                business_form=bf,
                tax_number='{xxxxxxxx}-{y}-{zz}'.format(
                    xxxxxxxx=randint(10000000, 99999999),
                    y=randint(1, 5),
                    zz=randint(1, 40),
                )
            )

    def generate_individuals(self, amount=5):
        """
        Példa egyéni vállalkozások generálása
        :return:
        """
        for index in range(0, amount):
            person = choice(Person.objects.all())
            Individual.objects.create_individual(
                owner=person,
                name='{display_name} EV'.format(display_name=person.full_name)
            )

    def log_pauses(self):

        c11 = PauseCategory.objects.get(code="11")
        c41 = PauseCategory.objects.get(code="41")
        c71 = PauseCategory.objects.get(code="71")

        d_2020_06_01 = datetime(year=2020, month=6, day=1)
        d_2020_06_30 = datetime(year=2020, month=6, day=30)
        d_2020_01_15 = datetime(year=2020, month=1, day=15)
        d_2020_01_29 = datetime(year=2020, month=1, day=29)

        Pause.objects.create(category=c11, begin=d_2020_06_01, end=d_2020_06_30)
        Pause.objects.create(category=c41, begin=d_2020_01_15, end=d_2020_01_15)
        Pause.objects.create(category=c71, begin=d_2020_01_15, end=d_2020_01_29)

    def log_timesheets(self, salary: Salary, year: int, month: int):

        sheet = TimeSheet.objects.create(current_year=year, current_month=month)
        begin = datetime(year=year, month=month, day=1)
        end = datetime(year=year, month=month, day=calendar.monthrange(year, month)[1])
        for day in range(begin.day, end.day):
            presense_category = choice(TimeSheetCategory.objects.all())
            absense_category = choice(PauseCategory.objects.all())

            time = timedelta(hours=randint(2, 12))
            if choice([True, False]):
                TimeSheetItem.objects.create(
                    presence=presense_category,
                    sheet=sheet,
                    timestamp=datetime(year=year, month=month, day=day),
                    duration=time
                )
            else:
                TimeSheetItem.objects.create(
                    absence=absense_category,
                    sheet=sheet,
                    timestamp=datetime(year=year, month=month, day=day),
                    duration=time
                )
        salary.timesheet = sheet
        salary.save()

        sheet.prepare()
        sheet.summarize()

    def recruit(self, headcount=10):
        for head in range(1, headcount):
            employee = choice(Person.objects.all())
            employer = choice(Customer.objects.all())
            aq = choice(ApplianceQuality.objects.all())
            self._highlight(
                message='{employee}-t foglalkoztatása, {employer} által ({type})',
                employee=str(employee),
                employer=str(employer),
                type=str(aq)
            )
            employment = Employment.objects.create(
                employee=employee,
                employer=employer,
                type=aq,
            )

            self.generate_dependencies(amount=10, provider=employment)


    def pay_salaries(self, minimum: int = 100000, maximum: int = 10000000, begin: datetime = datetime(year=2018, month=1, day=1), end: datetime = datetime.now()):
        for employment in Employment.objects.all():
            for year in range(begin.year, end.year):
                for month in range(1, 12):


                    day = calendar.monthrange(year, month)[1] - 1
                    salary = randint(minimum, maximum)
                    self._highlight(
                        message = '{year}/{month}  {employer} -> {employee}: {salary} ({type})',
                        employee = str(employment.employee),
                        employer = str(employment.employer),
                        salary = salary,
                        type = str(employment.type),
                        year = year,
                        month = month,
                    )
                    s = Salary.objects.create(
                        employee=employment,
                        salary=salary,
                        begin=datetime(year=year, month=month, day=1),
                        end=datetime(year=year, month=month, day=day),
                    )

                    self.log_timesheets(salary=s,year=year, month=month)
                    self.generate_blocked_salaries(salary=s)

    def generate_blocked_salaries(self, salary: Salary, amount: int = 10, minimum: int = 0, maximum: int = 100000):
        for b in range(0, randint(0, amount)):
            SalaryBlockingItem.objects.create(
                salary=salary,
                value=randint(minimum, maximum),
                account=choice(BankAccount.objects.all()),
            )

    def generate_dependencies(self, provider: Employment, amount: int = 10):
        for d in range(0, randint(0, amount)):
            year = randint(1900, 2020)
            month = randint(1, 12)
            day = randint(*calendar.monthrange(year, month)) % 27 + 1
            q = choice(DependentQuality.objects.all())
            r = choice(DependentRight.objects.all())
            dependent = choice(Person.objects.all())
            Dependence.objects.create(
                dependent=dependent,
                provider=provider,
                quality=q,
                right=r,
                begin=datetime(year=year, month=month, day=day),
                end=datetime(year=year+randint(1, 10), month=month, day=day),
            )

    def _highlight(self, message: str, **kwargs):
        self.stdout.write(message.format(
            **kwargs
        ))