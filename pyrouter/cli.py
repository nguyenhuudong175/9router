import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="9router")
    parser.add_argument("--port", "-p", type=int, default=20128)
    parser.add_argument("--host", "-H", default="0.0.0.0")
    parser.add_argument("--version", "-v", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("0.1.0")
        return 0

    print(f"9router python migration bootstrap | host={args.host} port={args.port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
