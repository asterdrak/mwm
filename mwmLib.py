#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pickle;

class rok:
	def __init__ (self, numer):
		"""podobiekty drużyn. konkretne lata które obrazują stan składek drużyny, ich liczbę i wartość."""
		self.ad = numer;
		self.stawka = [0]*12;
		self.liczba = [0]*12;
		self.wplaty = [0]*12;
		self.nadplata = 0;
	def ustawStawke(self, przedzialStart, przedzialKoniec, stawka):
		"""ustawia stawkę na jednego harcerza na określone miesiące (z przedziału)"""
		przedzialStart -= 1;
		while przedzialStart < przedzialKoniec:		
			self.stawka[przedzialStart] = stawka;
			przedzialStart += 1;
		return 1;
	def ustawLiczbe(self, przedzialStart, przedzialKoniec, liczba):
		"""ustawia liczbę harcerzy w określonych miesiącach (z przedziału)"""
		przedzialStart -= 1;
		while przedzialStart < przedzialKoniec:		
			self.liczba[przedzialStart] = liczba;
			przedzialStart += 1;
		return 1;
	def stan(self):
		"""sprawdza stan całego roku - jeśli nie wszystko jest opłacone zwraca (0), jeśli jest zwraca (1, nadpłata)"""
		for i in range(12):
			if self.wplaty[i] != self.stawka[i]*self.liczba[i]:
				return (0, 0);
		return (1, self.nadplata);
	def zaplac(self, kwota):
		"""wprowadza daną kwotę i rozprowadzą ją odpowiednio po kolejnych miesiącach - uzupełnie do maksymalnej kwoty wyliczanej z
		przemnożonej liczby członków przez stawkę. Przepełnieniona kwota wchodzi w nadpłatę"""
		for i in range(12):
			if self.wplaty[i] < self.stawka[i]*self.liczba[i] and kwota > 0:
				kwota -= self.stawka[i]*self.liczba[i]-self.wplaty[i];
				self.wplaty[i] += self.stawka[i]*self.liczba[i]-self.wplaty[i];
				if kwota < 0:
					self.wplaty[i] += kwota;
					kwota = 0;
		self.nadplata += kwota;
		return 1;
	def cenaMiesiace(self, przedzialStart, przedzialKoniec):
		"""szacuje cenę miesięcy z zadanego przedziału tylko z tego roku, jeśli koniec przedziału jest mniejszy od przedziały
		zwraca do początku do grudnia, następny rok szacuje metoda z klasy rodzica"""
		if przedzialStart > 12 or przedzialKoniec > 12 or przedzialKoniec < 1 or przedzialStart < 1:		
			return (0, 0, 0);
		if przedzialStart < przedzialKoniec:
			suma = 0;
			while przedzialStart <= przedzialKoniec:
				suma += self.stawka[przedzialStart-1]*self.liczba[przedzialStart-1]-self.wplaty[przedzialStart-1];
				przedzialStart += 1;
			return (1, suma, 0);
		if przedzialStart > przedzialKoniec:
			suma = 0
			while przedzialStart <= 12:
				suma += self.stawka[przedzialStart-1]*self.liczba[przedzialStart-1]-self.wplaty[przedzialStart-1];
				przedzialStart += 1;
			return (0, suma, przedzialKoniec);
				
			
				
		

class jednostka:
	def __init__ (self, nazwa):
		self.data = {
		"nazwa": nazwa,
		"druzynowy": "Imię i nazwisko drużynowego",
		"hufiec": "Nazwa hufca",
		"komentarz": "Bez komentarza",
		"stan": "czynna",
		"dlug": 0};
		self.lata = {};
		self.stawka = 0;
	def dodajRok(self, nrrok):
		"""dodaje nowy rok o kluczu nrrok do słownika lat"""
		self.lata[nrrok] = rok(nrrok);
		try:
			self.lata[nrrok].ustawLiczbe(1, 12, self.lata[nrrok-1].liczba[12-1]);
			self.lata[nrrok].ustawStawke(1, 12, self.lata[nrrok-1].stawka[12-1]);
		except KeyError:
			pass;
		self.lata[nrrok].stawka = [self.stawka]*12;
		return 1;
	def zamknijRok(self, nrrok):
		"""zamyka rok jeśli wszystko jest opłacone, otwiera nowy i opłaca nadpłatą bieżącego
		w przypadku sukcesu usuwa element słownika lat"""
		try:
			stan = self.lata[nrrok].stan();
		except KeyError:
			return 0;
		if(stan[0] == 1):
			if stan[1] > 0:
				try:
					self.lata[nrrok+1].zaplac(stan[1]);
				except KeyError:
					self.dodajRok(nrrok+1);
					self.lata[nrrok+1].zaplac(stan[1]);
			del self.lata[nrrok];
			return 1;
		else:
			return 0;
	def wymus_zamknijRok(self, nrrok):
		"""wymusza zamknięcie roku, oblicza brakującą kwotę i dodaje do długu jednostki;
		usuwa element słownika lat"""
		try:
			self.data["dlug"] += self.ocenMiesiace(nrrok, 1, 12);
			self.data["dlug"] -= self.lata[nrrok].nadplata;
		except KeyError:
			return 0;
		self.dodajRok(nrrok+1);
		del self.lata[nrrok];

		return 1;
	def zaplacRok(self, nrrok, kwota):
		"""opłaca zadany (o numerze nrrok) kwotą (kwota)
		jeśli pojawia się nadpłata próbuje zamknąc rok i opłacić następny (przez zamykanie roku)"""
		try:
			self.lata[nrrok].zaplac(kwota);
		except KeyError:
			return 0;
		if self.lata[nrrok].nadplata > 0:
				self.zamknijRok(nrrok)
		return 1;
	def ocenMiesiace(self, nrrok, przedzialStart, przedzialKoniec):
			"""ocenia kwotę do zapłaty z zadanego przedziały miesięcy
			maksymalnie do 24 miesięcy"""
			try:
				wynik = self.lata[nrrok].cenaMiesiace(przedzialStart, przedzialKoniec);
			except KeyError:
				return 0;
			if wynik[0] == wynik[1] == wynik[2] == 0:
				return "InputError";
			elif wynik[0] == 0 and wynik[2] > 0:
				try:
					self.lata[nrrok+1];
				except KeyError:
					self.dodajRok(nrrok+1);
				return wynik[1]+self.lata[nrrok+1].cenaMiesiace(1, wynik[2])[1];
			elif wynik[0] == 1:
				return wynik[1];#zwraca sumę
					
	


class base:
	def __init__ (self):
		self.bRok = 2015;
		self.bMiesiac = 2;
		self.druzyny = {};
		self.instruktorzy = {};
		self.data = {};
		try:
			f = open("/tmp/mwmDump.dat", "r");
			t = pickle.load(f);
		    	self.druzyny = t[0];
			self.instruktorzy = t[1];
			self.data = t[2];
			f.close();
			return None;
		except IOError:
			pass;
		self.data["stawkaDruzyny"] = 9.5;
	def dodajDruzyne(self, nazwaKrotka, nazwaPelna):
		"""dodaje drużyne o zadanym kluczu i pełnej nazwie"""
		self.druzyny[nazwaKrotka] = jednostka(nazwaPelna);
		self.druzyny[nazwaKrotka].stawka = self.data["stawkaDruzyny"];
	def listujDruzyny(self):
		"""zwraca listę drużyn"""
		return self.druzyny.keys();
	def szukajJednostki(self, query):
		"""Zwraca listę drużyn, które zawierają w którymkolwiek polu wyrażenie query"""
		pass;													#napisać!!!
	def serialize(self):
		"""serializuje się do pliku"""
		f = open("/tmp/mwmDump.dat", "w");
		pickle.dump((self.druzyny, self.instruktorzy, self.data), f);
		f.close();





