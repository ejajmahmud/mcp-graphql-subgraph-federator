"""Unit tests for mcp-graphql-subgraph-federator."""
import unittest
from mcp_graphql_subgraph_federator.federator import SubgraphFederator, SubgraphDef

class TestSubgraphFederator(unittest.TestCase):
    def setUp(self):
        self.fed = SubgraphFederator()

    def test_federate_multiple_subgraphs(self):
        self.fed.register_subgraph(SubgraphDef("billing", "http://bill/gql", ["Invoice"], {"getInvoice": {"id": "string"}}))
        self.fed.register_subgraph(SubgraphDef("catalog", "http://cat/gql", ["Item"], {"searchItems": {"query": "string"}}))

        tools = self.fed.list_mcp_tools()
        self.assertEqual(len(tools), 2)
        names = [t["name"] for t in tools]
        self.assertIn("billing_getInvoice", names)
        self.assertIn("catalog_searchItems", names)
