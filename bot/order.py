from response import Response


class RoomOrder:
	def __init__(self):
		self.rooms = {};

	def new_order(self, room, order_name):
		if room in self.rooms:
			return Response.text(Response.REP_DUP_ORDERLIST)
		else:
			self.rooms[room] = Order(order_name)
			return Response.text(Response.REP_NEW_ORDERLIST_CREATED, order_name)

	def get_order(self, room):
		return self.rooms[room]

	def list_order(self, room):
		try:
			order = self.rooms[room]
			return Response.text(Response.REP_SUMMARY_ORDERLIST, order.name, order.order_by_menu_string(), order.order_by_user_string())
		except KeyError:
			return None

	def end_order(self, room):
		name = self.rooms[room].name
		del self.rooms[room]
		return Response.text(Response.REP_END_ORDERLIST, name)


class Order:
	def __init__(self, name):
		self.name = name
		self.enable = True
		self.order_by_menu = {}
		self.order_by_user = {}

	def add_order(self, user, menu, amount=1):
		if self.enable:
			return Response.text(Response.REP_NOT_IMPLEMENT)
		else:
			return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

	def del_order(self, user, menu, amount=-1):
		if self.enable:
			return Response.text(Response.REP_NOT_IMPLEMENT)
		else:
			return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

	def setEnable(self, flag):
		self.enable = flag

	def order_by_menu_string(self):
		text = ""
		for menu, amount in self.order_by_menu:
			text += "%s %d" % (menu, amount) + "\n"
		return text[:-1]

	def order_by_user_string(self):
		text = ""
		for user, order in self.order_by_user:
			text += user + "\n"
			for menu, amount in order:
				text += menu + " " + amount + "\n"
		return text[:-1]

	def list_order_by_menu(self):
		return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_menu_string)

	def list_order_by_user(self):
		return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_menu_user)

	def __str__(self):
		return self.order_by_user_string()
