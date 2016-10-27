import subprocess, os
from getfile import get_voc_file



def get_clipboard():
	return subprocess.check_output(["xsel", "-a"])


def main():
	
	my_dir = os.path.dirname(os.path.abspath(__file__))
	
	base = os.path.join(my_dir, 'data/')

	words = get_clipboard()
	
	
	for rword in words.split():
		word = rword.strip(' .;:,\t-\n()[]{}?/$!\'').lower()
		
		if not word:
			print("empty word -- skipping")
			continue
		
		path = os.path.join(base, word+'.mp3')
		
		print 'path =', path
		
		if not os.path.isfile(path):
			print 'downloading', word
			get_voc_file(word, path)
		
		# touch
		open(path, 'a').close()
		
		
		if os.path.isfile(path) and os.path.getsize(path) > 0:
			fname = '{}.mp3'.format(word)
		else:
			fname = 'beep28917.wav'

		subprocess.call(['mplayer', os.path.join(base, fname)])
			
	else:
		print("empty word -- skipping")
	

if __name__ == '__main__':
	main()	
