all: lint

        #--const-naming-style=camelCase          \

LINT_FLAGS=                                     \
        --const-rgx='[a-zA-Z0-9_]+'             \
        --argument-naming-style=camelCase       \
        --attr-naming-style=camelCase           \
        --class-naming-style=camelCase          \
        --function-naming-style=camelCase       \
        --method-naming-style=camelCase         \
        --variable-naming-style=camelCase       
lint:
	pylint $(LINT_FLAGS) announce.py config.py
