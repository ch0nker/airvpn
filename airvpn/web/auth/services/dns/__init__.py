from __future__ import annotations

from airvpn.web.auth.services.common import ClientService, WebSession
from airvpn.exceptions import ValidationError

from bs4 import BeautifulSoup

import json

from .models import Current, DnsList, Answer, Record, AnswerType, ActionType, RecordType

class DnsManager(ClientService):
    """Manages the authenticated user's custom DNS configuration.

    Wraps the AJAX endpoints behind ``https://airvpn.org/dns/`` to view
    available DNS lists and toggle or edit the user's custom DNS selection.

    Attributes:
        lists (list[Dns]): All DNS lists currently available.
        current (Current): The user's currently active DNS configuration.
        device (str | None): The device this configuration applies to, if any.
    """
    __URL__ = "https://airvpn.org/dns/"
    def __init__(self, session: WebSession, device: str | None = None):
        super().__init__(DnsManager.__URL__, session)
        self.lists: list[DnsList] = []
        self._lists_map = {}
        self.current = Current([], False)
        self.device = device
        self.update()

    def update(self):
        """Refresh `lists` and `current` from the server.

        Fetches the DNS page and parses the embedded JSON data to
        repopulate `lists`, the internal DNS lookup map, `current`,
        and `device`.
        """
        response = self.session.request("get", DnsManager.__URL__, params={"device": self.device})
        soup = BeautifulSoup(response.text, "html.parser")

        dns_data = soup.find("div", id="air_pages_dns_data")
        data = json.loads(dns_data.get("data-json"))

        current = data.get("current")

        self.current.enabled = current.get("custom")
        self.current.lists = current.get("lists")
        self.device = data.get("device")

        self.lists = []
        self._lists_map = {}
        for dns in data.get("lists", []):
            dns = DnsList(**dns)
            self.lists.append(dns)
            self._lists_map[dns.code] = dns

    def get_list(self, dns: DnsList | str):
        """Resolve a DNS list to a `Dns` instance.

        Args:
            dns: `Dns` instance or DNS list code to resolve.

        Returns:
            The matching `Dns` instance.

        Raises:
            ValidationError: If `dns` is a string code that doesn't match
                any known DNS list.
        """
        if isinstance(dns, str):
           _dns = self._lists_map.get(dns)
           if _dns is None:
               raise ValidationError(f"Failed to find dns \"{dns}\"")
           dns = _dns

        return dns

    def save(self):
        """Persist the current DNS configuration to the server."""
        self.request("save", data=json.dumps(self.current.to_json()))

    def toggle(self):
        """Toggle custom DNS on or off and save the change."""
        self.current.enabled = not self.current.enabled
        self.save()

    def add_record(self, answer: Answer, type: RecordType, value: str) -> Record:
        """Create a record, attach it to an answer, and save the change.

        Args:
            answer: The `Answer` instance to attach the new record to.
            type: The `RecordType` of the record to create (e.g. A, AAAA, CNAME).
            value: The record's value (e.g. an IP address or hostname).

        Returns:
            The `Answer` the record was added to.
        """
        record = Record(type, value)
        answer.records.append(record)

        self.save()

        return answer

    def remove_record(self, answer: Answer, record: Record):
        """Remove a record from an answer's record list and save the change.

        Args:
            answer: The `Answer` instance containing the record.
            record: The `Record` instance to remove.

        Raises:
            ValueError: If `record` is not present in `answer.records`.
        """
        answer.records.remove(record)
        self.save()

    def add_answer(self,
               host: str,
               type: AnswerType = AnswerType.EXACT, 
               action: ActionType = ActionType.DENY,
               records: list[Record] = []) -> Answer:
        """Create a new answer rule and add it to the current configuration.

        Args:
            host: The hostname or pattern the rule matches against.
            type: How `host` is matched (e.g. exact, wildcard). Defaults to
                `AnswerType.EXACT`.
            action: The action to take when the rule matches (e.g. allow,
                deny). Defaults to `ActionType.DENY`.
            records: Initial list of `Record` instances to attach to the
                answer. Defaults to an empty list.

        Returns:
            The newly created `Answer`.
        """
        answer = Answer(type, host, action, records)

        self.current.answers.append(answer)
        self.save()

        return answer

    def remove_answer(self, answer: Answer):
        """Remove an answer from the current DNS configuration and save the change.

        Args:
            answer: The `Answer` instance to remove.

        Raises:
            ValueError: If `answer` is not present in `self.current.answers`.
        """
        self.current.answers.remove(answer)
        self.save()

    def add_list(self, dns: DnsList | list[DnsList] | list[str] | str):
        """Add one or more DNS lists to the current configuration.

        Args:
            dns: A `Dns` instance, DNS list code, or a list of either,
                to add to the current selection.
        """
        if isinstance(dns, list[DnsList]):
            items: list[str] = []
            for item in dns:
                items.append(item.code)
            dns = items

        if isinstance(dns, list[str]):
            self.current.lists.extend(dns)
            self.save()
            return

        dns = self.get_list(dns)
        if dns.code in self.current.lists:
            return

        self.current.lists.append(dns.code)
        self.save()

    def remove_list(self, dns: DnsList):
        """Remove a DNS list from the current configuration and save the change.

        Args:
            dns: The DNS list code (str) to remove from the current selection.

        Raises:
            ValueError: If `dns` is not present in `self.current.lists`.
        """
        self.current.lists.remove(dns)
        self.save()

    @classmethod
    def from_dns(cls, session: WebSession, device: str):
        """Create a `DnsManager` scoped to a specific device.

        Args:
            session: The `WebSession` to use for requests.
            device: The device identifier to scope the configuration to.

        Returns:
            A new `DnsManager` instance for the given device.
        """
        return cls(session, device)