from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime, timezone, timedelta
from corgy_common.models import Pretence
from corgy_common.models import Legal
from corgy_common.models import Tax
from corgy_common.models import Discount

from corgy_common.models import Pause
from corgy_common.models import PauseCategory

from corgy_common.models import Customer
from corgy_common.models import Individual
from corgy_common.models import Organization
from corgy_common.models import Person
from corgy_common.models import gender_male,gender_female, gender_choices
from corgy_common.models import Address
from corgy_common.models import BusinessForm

from corgy_common.models import TimeSheet
from corgy_common.models import TimeSheetCategory
from corgy_common.models import TimeSheetStatistic
from corgy_common.models import TimeSheetItem

class Command(BaseCommand):
    help = _('Személyre szabott törzsadatok generálása.')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        self.generate_categories_pause()
        self.stdout.write(self.style.SUCCESS("Biztosítás szünentelése törzs: létrehozva"))

        self.generate_categories_timesheet()
        self.stdout.write(self.style.SUCCESS("Jelenléti blokk törzs: létrehozva"))

        self.generate_taxes()
        self.stdout.write(self.style.SUCCESS("Adónemek törzs: létrehozva"))

        self.generate_legals()
        self.stdout.write(self.style.SUCCESS("Jogviszony törzs: létrehozva"))

        self.generate_pretences()
        self.stdout.write(self.style.SUCCESS("Jogcím törzs: létrehozva"))

        self.generate_business_forms()
        self.stdout.write(self.style.SUCCESS("Cégforma törzs: létrehozva"))

        self.generate_persons()
        self.stdout.write(self.style.SUCCESS("Személyi adatlapok generálása"))

        self.generate_individuals()
        self.generate_organizations()
        self.stdout.write(self.style.SUCCESS("Vállalkozások generálása"))

        self.log_pauses()
        self.log_timesheets()
        self.stdout.write(self.style.SUCCESS("Adatok generálása"))

    def generate_business_forms(self):
        """
        Laki-Studio cégformák törzs generálása
        :return:
        """
        BusinessForm.objects.all().delete()
        BusinessForm.objects.create(code="", name="Európai szövetkezet")
        BusinessForm.objects.create(code="", name="Külföldi székhelyű európai gazdasági egyesülés magyarországi telephelye")
        BusinessForm.objects.create(code="", name="Közjegyzői iroda")
        BusinessForm.objects.create(code="", name="Európai részvénytársaság")
        BusinessForm.objects.create(code="", name="Európai gazdasági egyesülés")
        BusinessForm.objects.create(code="", name="Végrehajtói iroda")
        BusinessForm.objects.create(code="", name="Külföldi vállalkozás magyarországi fióktelepe")
        BusinessForm.objects.create(code="", name="Vízgazdálkodási társulat")
        BusinessForm.objects.create(code="", name="Erdőbirtokossági társulat")
        BusinessForm.objects.create(code="", name="Közhasznú társaság")
        BusinessForm.objects.create(code="", name="Oktatói munkaközösség")
        BusinessForm.objects.create(code="", name="Külföldiek magyarországi közvetlen kereskedelmi képviselete")
        BusinessForm.objects.create(code="", name="Egyéni cég")
        BusinessForm.objects.create(code="", name="Részvénytársaság")
        BusinessForm.objects.create(code="kft", name="Korlátolt felelősségű társaság")
        BusinessForm.objects.create(code="", name="Közös vállalat")
        BusinessForm.objects.create(code="", name="Egyesülés")
        BusinessForm.objects.create(code="", name="Betéti társaság")
        BusinessForm.objects.create(code="", name="Jogi személy felelősségvállalásával működő gazdasági munkaközösség")
        BusinessForm.objects.create(code="", name="Gazdasági munkaközösség")
        BusinessForm.objects.create(code="", name="Közkereseti társaság")
        BusinessForm.objects.create(code="", name="Szövetkezet")
        BusinessForm.objects.create(code="", name="Vállalat")



    def generate_categories_timesheet(self):
        """
        Laki-Studio jelenléti blokk törzs generálása
        :return:
        """
        TimeSheetCategory.objects.all().delete()
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

    def generate_categories_pause(self):
        """
        Laki-Studió biztosítási törzsadatok generálása.
        :return:
        """
        PauseCategory.objects.all().delete()
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

    def generate_taxes(self):
        """
        Laki-Studio adónemek törzs generálása.
        :return:
        """
        Discount.objects.all().delete()
        Tax.objects.all().delete()

        Tax.objects.create(code="", name="Rehabilitációs hozzájárulás")

        Tax.objects.create(code="", name="Cégautóadó")

        szja = Tax.objects.create(code="", name="Személyi jövedelemadó")
        Discount.objects.create(tax=szja, name="Négy vagy több gyermeket nevelők kedvezménye")
        Discount.objects.create(tax=szja, name="Családi kedvezmény")
        Discount.objects.create(tax=szja, name="Első házasok kedvezménye")
        Discount.objects.create(tax=szja, name="Személyi kedvezmény")

    def generate_legals(self):
        """
        Laki-Studio saját jogviszony törzs generálása.
        :return:
        """
        Legal.objects.all().delete()

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

    def generate_pretences(self):
        """
        Laki-Studio saját jogcím törzs generálása.

        :return:
        """
        Pretence.objects.all().delete()
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

    def generate_persons(self):
        """
        Példa személyi addatlapok generálása
        :return:
        """
        Address.objects.all().delete()
        Person.objects.all().delete()

        address = Address.objects.create(street_number=11,route='Kócsag')

        self.ofelia_bartok = Person.objects.create(
            gender=gender_female,
            birthdate=datetime(year=1957, month=5, day=19),
            birthplace="Csengele",
            name_of_mother="Karczag Tímea",
            first_name="Ofélia",
            last_name="Bartók",
            permanent_address=address,
            nationality='hu',
            inland_resident=True,
            tax_number='0011344'
        )

        self.manfred_csele = Person.objects.create(
            gender=gender_male,
            birthdate=datetime(year=1980, month=6, day=11),
            birthplace="Szeged",
            name_of_mother="Boros Katalin",
            first_name="Manfréd",
            last_name="Csele",
            permanent_address=address,
            nationality='hu',
            inland_resident=True,
            tax_number='0011344'
        )

        self.csanad_bornemissza = Person.objects.create(
            gender=gender_male,
            birthdate=datetime(year=1933, month=3, day=23),
            birthplace="Budapest",
            name_of_mother="Varnusz Titánia",
            first_name="Csanád",
            last_name="Bornemissza",
            permanent_address=address,
            nationality='hu',
            inland_resident=True,
            tax_number='0011344'
        )



    def generate_organizations(self):
        """
        Példa társas vállakozások generálása
        :return:
        """
        Organization.objects.all().delete()

        Organization.objects.create(
            manager=self.manfred_csele,
            registration_number='123456',
            business_form=BusinessForm.objects.get(code='kft')
        )

    def generate_individuals(self):
        """
        Példa egyéni vállalkozások generálása
        :return:
        """
        Individual.objects.all().delete()

        Individual.objects.create(owner=self.csanad_bornemissza)

    def log_pauses(self):
        Pause.objects.all().delete()

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

    def log_timesheets(self):
        TimeSheetItem.objects.all().delete()
        TimeSheet.objects.all().delete()


        cX = TimeSheetCategory.objects.get(code="X")
        cF = TimeSheetCategory.objects.get(code="F")
        cI = TimeSheetCategory.objects.get(code="I")
        cS = TimeSheetCategory.objects.get(code="S")

        d_2020_06_01 = datetime(year=2020, month=6, day=1)
        d_2020_06_02 = datetime(year=2020, month=6, day=2)
        d_2020_06_03 = datetime(year=2020, month=6, day=3)
        d_2020_06_04 = datetime(year=2020, month=6, day=4)
        d_2020_06_05 = datetime(year=2020, month=6, day=5)
        d_2020_06_06 = datetime(year=2020, month=6, day=6)
        d_2020_06_07 = datetime(year=2020, month=6, day=7)

        t1 = timedelta(hours=1)
        t2 = timedelta(hours=2)
        t4 = timedelta(hours=4)
        t8 = timedelta(hours=8)

        sheet1 = TimeSheet.objects.create(current_year=2020, current_month=1)
        sheet2 = TimeSheet.objects.create(current_year=2020, current_month=2)
        sheet3 = TimeSheet.objects.create(current_year=2020, current_month=3)
        sheet4 = TimeSheet.objects.create(current_year=2020, current_month=4)
        sheet5 = TimeSheet.objects.create(current_year=2020, current_month=5)
        sheet6 = TimeSheet.objects.create(current_year=2020, current_month=6)

        TimeSheetItem.objects.create(category=cX, sheet=sheet1, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet1, timestamp=d_2020_06_01, duration=t2)
        TimeSheetItem.objects.create(category=cX, sheet=sheet1, timestamp=d_2020_06_01, duration=t4)
        TimeSheetItem.objects.create(category=cX, sheet=sheet1, timestamp=d_2020_06_01, duration=t2)
        TimeSheetItem.objects.create(category=cX, sheet=sheet1, timestamp=d_2020_06_01, duration=t4)

        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t8)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t2)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t2)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t4)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet2, timestamp=d_2020_06_01, duration=t1)

        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t2)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t8)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t8)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t8)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t8)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
        TimeSheetItem.objects.create(category=cX, sheet=sheet3, timestamp=d_2020_06_01, duration=t1)
