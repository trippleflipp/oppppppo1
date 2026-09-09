from service import HarvestService
from gui import HarvestApp


def main():
    service = HarvestService()
    app = HarvestApp(service)
    app.run()


if __name__ == "__main__":
    main()