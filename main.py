#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Projet Python NSI - Irwan, Mohamed, Pierre
Jeux: Mastermind
"""

from datetime import datetime as dt
from terminaltables import SingleTable
import csv
import random


SCORE_ASSOCIATION = {0: 0, 1: 1, 2: 3, 3: 8, 4: 20}
MASTER_SUITE = [random.randint(10, 25) for _ in range(4)]


class Player(object):
	"""docstring for Player"""
	def __init__(self, arg):
		super(Player, self).__init__()
		self.id = arg['Id']
		self.name = arg['Name']
		self.gender = arg['Gender']
		self.job = arg['Job']
		self.house = arg['House']
		self.wand = arg['Wand']
		self.patronus = arg['Patronus']
		self.species = arg['Species']
		self.blood_status = arg['Blood status']
		self.hair_color = arg['Hair colour']
		self.eye_color = arg['Eye colour']
		self.loyalty = arg['Loyalty']
		self.skills = arg['Skills']
		self.birth = arg['Birth']
		self.death = arg['Death']
		self.suite = [random.randint(10, 25) for _ in range(4)]
		self.score = []
	
	def __str__(self):
		return f"{self.name} a {self.score} points"

	def reset_suite(self):
		self.suite = [random.randint(10, 25) for _ in range(4)]

	def reset_score(self):
		self.score = []

	def average_score(self) -> float:
		score_total, score_length = sum(player.score), len(player.score)

		if score_total == 0 or score_length == 0:
			return 0.0
		
		return score_total / score_length

	def add_score(self, points: int):
		self.score.append(points)

	def run_game(self):
		"""Will run a game and add the points for the current player to their score list"""
		count = len([n for n in self.suite if n in MASTER_SUITE])
		points = SCORE_ASSOCIATION[count]
		self.add_score(points)
		self.reset_suite()
		print(count, points, MASTER_SUITE, self.suite, self.score)


def main():
	with open('characters.csv') as file:
		reader = csv.DictReader(file, delimiter=';')
		players = [Player(dict(row)) for row in reader]

	while True:
		ask_commands(players)


def ask_commands(players):
	command = input('>> Que voulez-vous faire? (jouer/reinitialiser/voir score/quitter) ')

	match command:
		case "jouer":
			play(players)
			print(f'10 parties par joueur ont été jouées.')
		case "reinitialiser":
			confirmation = input('>> Voulez-vous vraiment remettre à zéro le score de chaque joueurs? (oui/non) ')
			if confirmation.lower() == 'oui':
				reset_scores(players)
				print('Les scores ont été remis à zéro.')
			else:
				print('Rien a été changé.')
		case "voir score":
			show_score(players)
		case "quitter":
			print('Bonne journée!' if dt.now().hour < 19 else 'Bonne soirée!')
			exit()
		case other:
			print('Je n\'ai pas compris, pouvez-vous réessayer?')


def reset_scores(players: list[Player]):
	for player in players:
		player.reset_score()


def show_score(players):
	table = SingleTable([['Joueur', 'Score moyen', 'Maison']])
	table.title = 'Ordre décroissant'

	sorted_players = sorted(players, key=lambda player: sum(player.score), reverse=True)
	total_average = []

	for player in sorted_players:
		name, average_score, house = player.name, player.average_score, player.house
		total_average.append(average_score)
		table.table_data.append([name, f"{average_score:.2f}", house])

	if sum(total_average) != 0 and len(total_average):
		table.table_data.append(['Moyenne total des joueurs', f"{sum(total_average) / len(total_average):.2f}"])

	print(table.table)


def play(players: list[Player]):
	"""Will run x games for each players"""
	for player in players:
		for _ in range(10):
			player.run_game()


if __name__ == '__main__':
	main()
