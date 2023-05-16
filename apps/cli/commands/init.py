from command import Command


class Init(Command):
    @classmethod
    def configure(cls, subparsers):
        parser = subparsers.add_parser('init', description="Initialize linter into a codebase")
        parser.add_argument('target', help="project directory to initialize codebase index")
        parser.set_defaults(func=cls().run)

    def run(self, args):
        print(self, f"The target is {args.target}")
