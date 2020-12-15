import random

t = { # 0 - subject, 1 - object
  'author' : ["{1} is author of {0}"],
  'birthPlace' : ["{0} was born in the {1}.", 
                  "{1} is the place of birth of {0}"],
  'deathPlace' : ["{0} died in the {1}",
                  "{1} is the deathplace of {0}"],
  'director' : ["{0} is director of {1}"],
  'genre' : ["{0} plays in the {1} genre(s)."],
  'hometown' : ["Hometown of {0} is {1}",
                "{1} is hometown of {0}"],
  'language' : ["Language of {0} is {1}"],
  'literaryGenre' : ["{0} is written in the {1} genre."],
  'location' : ["{0} located in {1}"],
  'position' : ["Position of {0} is {1}"],
  'producer' : ["{0} is produser of {1}"],
  'recordLabel' : ["{0} was released on the {1}."],
  'timeZone' : ["{0} has the following time zone {1}",
                "{1} time zone is used in the {0}"],
  'writer' : ["Author of {0} is {1}"]
}


def make(predicate, subject, objectt):
  print(' Predicate: {} \n Subject: {} \n Object: {}'.format(predicate, subject, objectt))
  if subject == 'tag:/None':
    return 'No_data'
  if objectt[0] == 'tag:/None':
    return 'No_information'
  subject = subject.split('/')[-1]
  objectt_s = ''
  for s in objectt:
    objectt_s = '{}{}, '.format(objectt_s, s.split('/')[-1])
  predicate = predicate.split('/')[-1]
  tmps = t[predicate]
  i = random.randint(0, len(tmps)-1)
  return tmps[i].format(subject, objectt_s[:-2]).replace(' ', '_')

if __name__ == "__main__":
  subject, objectt = 'http://dbpedia.org/resource/Vasya', 'http://dbpedia.org/resource/Derevnya'
  tmp = make("birthPlace", subject, objectt)
  print(tmp)

