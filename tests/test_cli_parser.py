from energy_tagger.cli import build_parser


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["/tmp/music"])

    assert args.path == "/tmp/music"
    assert args.recursive is False
    assert args.field == "comment"
    assert args.dry_run is False
