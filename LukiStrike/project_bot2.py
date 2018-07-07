import requests
import sys

def get_user_url():
	qwestionsType=input("Выбери категорию вопроса: от 9 до 50 ")
	difficalty=input("Выбери сложность вопроса: easy/medium/hard ")
	userUrld="https://opentdb.com/api.php?amount=5&category=N&difficulty=D"
	userUrld=userUrld.replace("N",qwestionsType)
	userUrld=userUrld.replace("D",difficalty)
	return userUrld

def get_data(url):
	try:
		result=requests.get(url)
		if result.status_code==200:
			allContent=result.json()
			onlyHelpfullContent=allContent["results"]
			return 	onlyHelpfullContent
		else:
			print("Вопросы не получены. Попробуйте еще раз или обратитесь к администратору")
	except:
		print("Вероятно нет подключения к интернету. Попробуйте еще раз или обратитесь к администратору")
		sys.exit()

def get_count_questions(mass):
	maxCountQuestionsInMass=int(len(mass))
	if maxCountQuestionsInMass==0:
		print("Вопросы не получены. Попробуйте еще раз")
		sys.exit()
	return maxCountQuestionsInMass

def print_question_and_answers_and_get_correctIndexOfCorrectAnswer(number):
	question=data[number]
	print("Вопрос №",number+1,":")
	print(question.get("question"))
	answers=question.get("incorrect_answers")
	correctAnswer=question.get("correct_answer")
#	print("Верный ответ: ", correctAnswer)
	answers.append(correctAnswer)
	answers.sort()
	correctIndexOfCorrectAnswer=answers.index(correctAnswer)
	countAnswers=len(answers)
	print("Варианты ответа: ")
	i=0
	while i<countAnswers:
		print(i+1," ",answers[i])
		i+=1
	return correctIndexOfCorrectAnswer

def chek_answer(userAnswer,index):
	сorrectNumber=int(index+1)
	if userAnswer==сorrectNumber:
		print("Ответ верный,молодец!")
		returnDelta=0
	else:
		print("Упс...Ответ неверный")
		secondUserAnswerNumber=int(input("Попробуйте еще раз указать номер верного ответа: "))
		if secondUserAnswerNumber==сorrectNumber:
			print("Ответ верный,молодец!")
			returnDelta=0
		else:
			print("Упс...Ответ неверный")
			returnDelta=1	
	return returnDelta

def get_stop(countIncorrectUserAnswersForStop):
	if countIncorrectUserAnswersForStop==2:
		countIncorrectUserAnswersForStop=0
		markerContinue=input("Продолжаем? Да/Нет ")
		print()
		if markerContinue=="Нет":
			sys.exit()
	return countIncorrectUserAnswersForStop

if __name__ == '__main__':
	print("Привет!")
	# countQuestions - счетчик вопросов
	countQuestions=0
	# countIncorrectAnswers - счетчик неверных ответов
	countIncorrectUserAnswers=0
	# countIncorrectUserAnswersForStop - счечик неверных ответов для остановки
	countIncorrectUserAnswersForStop=0
	#настройка url в соответствии с введенной пользователем информацией
	userUrl=get_user_url()
	#получение вопросов с сайта
	data=get_data(userUrl)
	#вычисление общего количества вопросов, пришедших с сайта 
	maxCountQuestionsInData=get_count_questions(data)
	while countQuestions<maxCountQuestionsInData:
		try:
			correctIndex=int(print_question_and_answers_and_get_correctIndexOfCorrectAnswer(countQuestions))
			userAnswerNumber=int(input("Укажите номер верного ответа: "))
			delta=chek_answer(userAnswerNumber,correctIndex)
			countIncorrectUserAnswers=countIncorrectUserAnswers+delta
			countIncorrectUserAnswersForStop=countIncorrectUserAnswersForStop+delta
			print("Количество неверных ответов: ", countIncorrectUserAnswers)
			print("--------------------------------")	
			countIncorrectUserAnswersForStop=get_stop(countIncorrectUserAnswersForStop)
			countQuestions+=1
		except(IndexError,KeyboardInterrupt):
			print("Вопросы закончились")
			sys.exit()
		except(ValueError):
			print("ВНИМАНИЕ!Допустимо вводить только ЧИСЛОвые значения! Попробуйте еще раз")

