import pdf_compressor

pdf_file = 'merged.pdf'

key = 'project_public_778d413cc2b26d9a0715f38b579e2e13__2NA1bf7a78ab7ad461d3e550ab6472603d5d'
task = pdf_compressor.Compress(key)
task.add_file(pdf_file)
task.process()
task.download("./pdf")
task.delete_current_task()
