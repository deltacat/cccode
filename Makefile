## help: 打印本使用提示
.PHONY: help
help: Makefile
	@echo "Choose a command to run:"
	@sed -n 's/^##[ ]*//p' $< | column -t -s ':' |  sed -e 's/^/  /'

## clean: 删除输出文件
.PHONY: clean
clean:
	rm output/*

## walk: 遍历并输出源码文档
.PHONY: walk
walk:
	@./app.py