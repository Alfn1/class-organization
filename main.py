import grafofluxo as grafo


g1 = grafo.GrafoFluxo()
g1.read_file('disciplinas.csv','professores.csv')
r = g1.SMP()
g1.print_concl(r)