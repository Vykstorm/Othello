#!/usr/bin/python
# -*- coding: iso8859-1 -*-
# Autor: Víctor Ruiz Gómez
# Descripción: Este script permite graficar árboles (es muy útil para
# depurar el algoritmo Min-Max)

# Es necesaria la libreria et3
from ete3 import Tree, TreeStyle, TextFace, NodeStyle


class MinMaxTree:
	# Inicializa el árbol.
	def __init__(self, root_text):
		# Inicializa la estructura árbol
		tree = Tree()
		
		# Formateamos el árbol indicandole un estilo
		style = TreeStyle()
		style.show_leaf_name = True
		style.show_scale = False
		style.scale = 100
		style.branch_vertical_margin = 30
		style.rotation = 0
		style.orientation = 0
		self.style = style
		self.tree = tree
		
		# Le damos estilo a la raíz del árbol
		self.tree.add_face(TextFace(root_text, fsize=10, fgcolor='darkred'), column=0, position='branch-right')
		self.tree.set_style(NodeStyle(size=20, hz_line_width=2, fgcolor='blue'))
		
		# Almacenamos la raíz del árbol como nodo actual
		self.curr_node = self.tree
		
		
		
	# Añadimos un nuevo nodo (como hijo del último nodo procesado)
	# Esto hace que el último nodo procesado pase a ser el nodo nuevo creado.
	# Se le debe inicar como parámetro el texto que aparecerá en el nodo y el texto que
	# aparecerá en la arista. Por último, si el jugador es MAX o es MIN. Los nodos MÁX 
	# serán nodos azules mientras que los nodos MIN se repreentarán con nodos rojos.
	def add_node(self, node_text, edge_text, is_max):
		new = self.curr_node.add_child()
		new.add_face(TextFace(node_text, fsize=12, fgcolor='darkred'), column=0, position='branch-right')
		
		tf = TextFace(edge_text, fsize=9, fgcolor='darkgoldenrod')
		tf.margin_right = 30
		new.add_face(tf, column=0, position='branch-bottom')
		new.set_style(NodeStyle(size=14, fgcolor=('blue' if is_max else 'red')))
		self.curr_node = new
		
	# Este método establece que el siguiente nodo a procesar sea el nodo padre del último
	# nodo procesado (backtracing).
	def backtrace(self):
		if self.curr_node == self.curr_node.get_tree_root():
			return;
		self.curr_node = next(self.curr_node.iter_ancestors())
		
	# Establece el texto que se muestra al lado del nodo.
	def set_curr_node_value(self, text):
		tf = TextFace(text, fsize=9)
		tf.margin_right = 6
		self.curr_node.add_face(tf, column=0, position='branch-right')
		
	# Mostramos el árbol
	def show(self):
		self.tree.show(tree_style=self.style)
