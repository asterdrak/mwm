#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os;


help = """

Lista poleceń dostępnych w MwM:
	dodaj nazwaKluczDruzyny - dodawanie nowej drużyny
	pokaz nazwaKluczDruzyny [rok] - wyświetlanie informacji o drużynie
				 [i stanu podanego roku]
	exit - koniec programu
	clear - czyszczenie okna konsoli
	list - listowanie drużyn
	dane - wyświetlanie zmiennych środowiskowych
	ustawDaneDruzyny nazwaKluczDruzyny kluczZmiennej
	usunDruzyneNIE_UZYWAC nazwaDruzyny

""";


def clearScreen():#czyszczenie powłoki konsolowej. zmienić w windows!
	os.system("clear");


class consoleInterface:
	def __init__ (self, base):
		print "\n --------------Tryb konsolowy MwM beta--------------\n";
		self.base = base;
	def clear(self):
		"""czyści konsole, zaleznie od systemu - zmienić funkcję clearScreen"""
		clearScreen();
	def help(self):
		"""wyświetla treść globalnek zmiennej help"""
		print help;
	def dodaj(self, nazwaKrotka):
		"""dodaje druzynę o podanej nazwie, potem uzupełnia nazwę z raw_input()"""
		self.base.dodajDruzyne(nazwaKrotka, raw_input("Podaj pełną nazwę drużyny:"));
	def list(self):
		"""wypisuje listę kluczy drużyn"""
		print self.base.listujDruzyny();
	def zamknijRok(self, nazwaDruzyny, nrrok):
		self.base.druzyny[nazwaDruzyny].zamknijRok(int(nrrok));
	def zaplacRok(self, druzyna, nrrok, kwota):
		self.base.druzyny[druzyna].zaplacRok(int(nrrok), int(kwota));
	def ustawLiczbe(self, druzyna, nrrok, przedzialStart, przedzialKoniec, liczba):
		self.base.druzyny[druzyna].lata[int(nrrok)].ustawLiczbe(int(przedzialStart), int(przedzialKoniec), float(liczba));
	def dane(self):
		"""wyświetla zmienne środowiskowe"""
		for i in self.base.data.keys():
			print str(i)+": "+str(self.base.data[i]);
			return 1;
	def ustawDane(self, nazwa):
		"""ustawia element słownika z danymi głównego obiektu o indexie nazwa"""
		istr = raw_input();
		try:
			istr = float(istr);
		except ValueError:
			pass;
		self.base.data[nazwa] = istr;
	def dodajRok(self, nazwaDruzyny, nrrok):
			try:
				self.base.druzyny[nazwaDruzyny].dodajRok(int(nrrok));
			except KeyError:
				print "błąd32";
	def usunDruzyneNIE_UZYWAC(self, key):
		"""trwale usuwa drużyne o podanym kluczu"""
		try:
			del self.base.druzyny[key];
		except KeyError:
			pass;
	def ustawDaneDruzyny(self, nazwa, key):
		"""ustawia dane drużyny (nazwa) w słowniku o zadanym (key) indexie na wczytane z klawiatury"""
		try:
			self.base.druzyny[nazwa].data[key] = raw_input();
			return 1;
		except KeyError:
			return 0;
	def pokaz(self, nazwa, rok = 0):
		"""wyświetla dane drużyny i jeśli jest podany: rok"""
		try:
			obj = self.base.druzyny[nazwa];
		except KeyError:
			return 0;
		self.clear();
		for i in obj.data:
			print str(i)+": "+str(obj.data[i]);
		print "Lata: " + str(list(i for i in obj.lata));
		if rok != 0:
			try:
				print "\n";	
				for j in obj.lata[int(rok)].__dict__:
						print "Rok "+str(rok)+": "+str(j)+": "+str(obj.lata[int(rok)].__dict__[j]);
				print "\n";	
			except KeyError:
				pass;
	def exit(self):
		"""wypisuje zakończenie konsolowego shella"""
		print "Koniec Shella";
		return 0;
	def shell(self):
		"""GŁÓWNY SHELL - PRZECHWYTUJE POLECENIA Z KLAWIATURY, PRZERABIA NA ZAPIS FUNKCYJNY I WYWOŁUJE PRZECHWYTUJAC WYJĄTKI"""
		s = ""; #----------------------string wczytywany i obrabiany do funkcji
		w = ""; #-------------------string wynikowy z zapisem funkcyjnym do wykonania
		l = []; #-------------------------lista operacyjna - tymczasowa
		while w != "exit()":
			a = raw_input("mwm: ");
			l = a.split(" ");
			w = l[0];
			l.remove(l[0]);
			s = "\", \"".join(l);
			if s != '':
				s = '"'+s+'"';
			s = "("+s+")";
			w = ""+w+s;
			#print w;
			try: 
			  exec("self."+w);
			#except KeyError:
			except (NameError, TypeError, SyntaxError, AttributeError, KeyError):
			  print "Błędne polecenie";
			self.base.serialize();


