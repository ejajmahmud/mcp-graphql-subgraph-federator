"""CLI for mcp-graphql-subgraph-federator."""
import sys
import argparse
from .federator import SubgraphFederator, SubgraphDef

def main():
    parser = argparse.ArgumentParser(description="MCP GraphQL Subgraph Federator CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate compiling subgraphs to MCP tools")
    args = parser.parse_args()

    if args.demo:
        fed = SubgraphFederator()
        fed.register_subgraph(SubgraphDef(
            name="users",
            endpoint="https://api.internal/users/graphql",
            entities=["User", "Profile"],
            queries={"getUserById": {"userId": "string"}}
        ))
        fed.register_subgraph(SubgraphDef(
            name="orders",
            endpoint="https://api.internal/orders/graphql",
            entities=["Order"],
            queries={"getOrdersByCustomer": {"customerId": "string", "limit": "integer"}}
        ))
        tools = fed.list_mcp_tools()
        print(f"Compiled {len(tools)} MCP tools:")
        for t in tools:
            print(f"  - {t['name']}: {t['description']}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
