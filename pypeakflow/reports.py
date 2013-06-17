import logging
import sys
import os
import re
from peakflow_soap import PeakflowSOAP 


class Report:
    def __init__(self):
        self.pf = PeakflowSOAP()

    def get_graph(self, graph_id, output_filename, title = None):
        query = """
            <peakflow version="1.0">
                <query id="query1" type="traffic">
                    <time start_ascii="24 hours ago" end_ascii="now"/>
                    <unit type="bps"/>
                    <search limit="100" timeout="30"/>
                    <class>in</class>
                    <class>out</class>
                    <filter type="customer">
                        <instance value="%d"/>
                    </filter>
                </query>
            </peakflow>
            """ % int(graph_id)

        gc = """<?xml version="1.0" encoding="utf-8"?>
            <peakflow version="2.0">
            <graph id="graph1">
            <title>Foo</title>
            <ylabel>bps</ylabel>
            <width>800</width>
            <height>300</height>
            <legend>1</legend>
            </graph>
            </peakflow>
            """

        res = self.pf.getTrafficGraph(query, gc)

        f = open(output_filename, "w")
        f.write(res['graph'])
        f.close()




if __name__ == '__main__':
    logger = logging.getLogger()
    log_stream = logging.StreamHandler()
    log_stream.setFormatter(logging.Formatter("%(asctime)s: %(levelname)-8s %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_stream)

    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-H", "--host", help="host for SOAP API connection, typically the leader")
    parser.add_option("-U", "--username", help="username for SOAP API connection")
    parser.add_option("-P", "--password", help="password for SOAP API connection")
    parser.add_option("--graph-id", metavar="ID", help="get a graph for customer with id ID")
    parser.add_option("--output-file", metavar="FILE", help="write output to FILE")
    (options, args) = parser.parse_args()

    pf = PeakflowSOAP(options.host, options.username, options.password)

    if options.graph_id and not options.output_file:
        print >> sys.stderr, "Please provide an output file to write the graph to with --output-file"
        sys.exit(1)

    f = Report()
    f.get_graph(options.graph_id, options.output_file)
