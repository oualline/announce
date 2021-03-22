GUI=MainWindow.py configEdit.py listEdit.py announceEdit.py backgroundEdit.py
PYTHON=                 \
    announceEditMain.py   \
    backgroundEditMain.py   \
    configEditMain.py   \
    default.py          \
    listEditMain.py     \
    main.py             \
    mainWindowMain.py	\
    transitions.py      \
    util.py

all: $(GUI)

install: all $(PYTHON)
	cp $(GUI) $(PYTHON) ../bin

MainWindow.py: mainWindow.ui
	pyuic5 mainWindow.ui >MainWindow.py

configEdit.py: configEdit.ui
	pyuic5 configEdit.ui >configEdit.py

listEdit.py: listEdit.ui
	pyuic5 listEdit.ui >listEdit.py

announceEdit.py: announceEdit.ui
	pyuic5 announceEdit.ui >announceEdit.py

backgroundEdit.py: backgroundEdit.ui
	pyuic5 backgroundEdit.ui >backgroundEdit.py


dist: all
	(cd ..;tar cf /tmp/announce.0.5.tar gui/*.py gui/*.ui *.odt *.pdf bin/announce.py bin/config.py announce.d/train* announce.d/trolley* config.announce/thomas.txt config.announce/train.on.hour.txt \
		config.background/thomas.music.txt config.background/rr.songs.txt general.d/safe.mp3 songs.d/silence.mp3 ./readme.txt bin/Makefile gui/Makefile)
	gzip -9v /tmp/announce.0.5.tar
 

LINT_FLAGS=                                     \
        --const-rgx='[a-zA-Z0-9_]+'             \
        --argument-naming-style=camelCase       \
        --attr-naming-style=camelCase           \
        --class-naming-style=camelCase          \
        --function-naming-style=camelCase       \
        --method-naming-style=camelCase         \
	--module-naming-style=camelCase		\
        --variable-naming-style=camelCase       \
	--disable=R0401,W1510
lint:
	PYTHONPATH=../bin pylint $(LINT_FLAGS) $(PYTHON)
