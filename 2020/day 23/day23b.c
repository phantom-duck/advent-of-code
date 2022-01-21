#include <stdio.h>
#include <stdlib.h>

/************************** Circular list ******************************/

typedef struct _node {
	int data;
	struct _node *next;
} circ_node;
typedef circ_node* circ;

circ new_empty_circ()
{
	return NULL;
}

int isempty(circ c)
{
	if (c == NULL) return 1;
	else return 0;
}

void push_after_head(circ c, int value)
{
	circ_node *new_node;
	new_node = malloc(sizeof(*new_node));
	new_node->data = value;
	
	new_node->next = c->next;
	c->next = new_node;
}

void push_and_move(circ *c, int value)
{
	circ_node *new_node;
	new_node = malloc(sizeof(*new_node));
	new_node->data = value;
	
	if (isempty(*c)) {
		new_node->next = new_node;
		*c = new_node;
	}
	new_node->next = (*c)->next;
	(*c)->next = new_node;
	(*c) = (*c)->next;
}

int pop_after_head(circ c)
{
	circ_node *n;
	int ret;
	
	n = c->next;
	ret = n->data;
	c->next = c->next->next;
	free(n);
	return ret;
}
/***********************************************************************/

circ_node *matching_nodes[1000001];
int main()
{
	circ list = new_empty_circ();
	int i, T, x, y, z, curr_cup, destination, N = 1000000;
	
	/****** Push given input data *********/
	push_and_move(&list, 3);
	matching_nodes[3] = list;
	push_and_move(&list, 1);
	matching_nodes[1] = list;
	push_and_move(&list, 8);
	matching_nodes[8] = list;
	push_and_move(&list, 9);
	matching_nodes[9] = list;
	push_and_move(&list, 4);
	matching_nodes[4] = list;
	push_and_move(&list, 6);
	matching_nodes[6] = list;
	push_and_move(&list, 5);
	matching_nodes[5] = list;
	push_and_move(&list, 7);
	matching_nodes[7] = list;
	push_and_move(&list, 2);
	matching_nodes[2] = list;
	/**************************************/
	
	for (i=10; i<=1000000; i++) {
		push_and_move(&list, i);
		matching_nodes[i] = list;
	}
	list = list->next;
	
	for (T=0; T<10000000; T++) {
		curr_cup = list->data;
		x = pop_after_head(list);
		y = pop_after_head(list);
		z = pop_after_head(list);
		
		destination = ((curr_cup - 1) + N - 1) % N + 1;
		if (destination == x || destination == y || destination == z) {
			destination = ((destination - 1) + N - 1) % N + 1;
		}
		if (destination == x || destination == y || destination == z) {
			destination = ((destination - 1) + N - 1) % N + 1;
		}
		if (destination == x || destination == y || destination == z) {
			destination = ((destination - 1) + N - 1) % N + 1;
		}
		
		push_after_head(matching_nodes[destination], z);
		matching_nodes[z] = matching_nodes[destination]->next;
		push_after_head(matching_nodes[destination], y);
		matching_nodes[y] = matching_nodes[destination]->next;
		push_after_head(matching_nodes[destination], x);
		matching_nodes[x] = matching_nodes[destination]->next;
		
		list = list->next;
	}
	
	printf("%d %d\n", matching_nodes[1]->next->data, matching_nodes[1]->next->next->data);
	return 0;
}
