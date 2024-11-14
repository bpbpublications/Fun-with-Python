import click
from O365 import Account, MSGraphProtocol


def get_venets(client_id, secret_id, user):
    credentials = (client_id, secret_id)
    protocol = MSGraphProtocol()
    scopes = ["https://graph.microsoft.com/.default"]
    account = Account(credentials, protocol=protocol)
    if not account.is_authenticated:
        if account.authenticate(scopes=scopes):
            print("Authenticated")
    schedule1 = account.schedule(resource=f"{user}@hotmail.com")
    calendar1 = schedule1.get_default_calendar()
    events = calendar1.get_events(include_recurring=False)
    print("events:")
    for ev in events:
        print(dir(ev))
        print(ev)


@click.command()
@click.option("--user", type=str, help="user email", required=True)
@click.option("--client-id", type=str, help="client ID", required=True)
@click.option("--secret", type=str, help="client secret", required=True)
def main(client_id, secret, user):
    get_venets(client_id, secret, user)


if __name__ == "__main__":
    main()
