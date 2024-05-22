# Copyright 2024 Broda Group Software Inc.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
# Created:  2024-04-15 by eric.broda@brodagroupsoftware.com

import json

from cli import main

# Global state variables

# Common for all CLI commands
HOST="localhost"
PORT="20000"


#####
# MONITOR
#####


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT monitor \
#     --health
def test_cli_monitor_health():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "monitor",
        "--health"
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) > 0
    assert "osc-dm-proxy-srv" in result
    assert "osc-dm-registrar-srv" in result
    assert "osc-dm-search-srv" in result

# python ./src/cli.py $VERBOSE --host $HOST --port $PORT monitor \
#     --metrics
def test_cli_monitor_metrics():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "monitor",
        "--metrics"
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) > 0

