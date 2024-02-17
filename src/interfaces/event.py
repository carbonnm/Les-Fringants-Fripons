from abc import ABC

from ..enums.event_type import EventType


class Event(ABC):
	def __init__(self):
		self.listeners = []
		self.handlers = {}

	def register(self, listener):
		self.listeners.append(listener)
		for event_type in listener.listened_event_types:
			if event_type not in self.handlers:
				self.handlers[event_type] = []
			self.handlers[event_type].append(listener)

	def unregister(self, listener):
		if listener in self.listeners:
			self.listeners.remove(listener)
		for event_type in listener.listened_event_types:
			if event_type in self.handlers:
				self.handlers[event_type].remove(listener)

	def unregister_listener_for_event_type(self, listener, event_type):
		if event_type in self.handlers and listener in self.handlers[event_type]:
			self.handlers[event_type].remove(listener)

	def has_listener(self, event_type):
		if event_type in self.handlers:
			return len(self.handlers[event_type]) > 0
		return False

	def notify(self, event_types=None, *args, **kwargs):
		if event_types is None:
			event_types = []
		if isinstance(event_types, EventType):
			event_types = [event_types]
		if len(event_types) > 0:
			for event_type in event_types:
				if event_type in self.handlers:
					for listener in self.handlers[event_type]:
						listener.update(self, [event_type], *args, **kwargs)
		else:
			self.notify_all(self, *args, **kwargs)

	def notify_all(self, *args, **kwargs):
		for listener in self.listeners:
			listener.update(self, self.handlers.keys(), *args, **kwargs)