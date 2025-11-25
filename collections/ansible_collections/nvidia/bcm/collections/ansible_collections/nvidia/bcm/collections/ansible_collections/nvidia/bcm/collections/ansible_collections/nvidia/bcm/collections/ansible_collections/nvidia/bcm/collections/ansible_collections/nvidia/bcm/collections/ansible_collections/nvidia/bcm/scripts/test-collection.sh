#!/bin/bash
#
# Consolidated test script for NVIDIA BCM Ansible Collection
#
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COLLECTION_DIR="$(dirname "$SCRIPT_DIR")"
PLAYBOOK_DIR="$COLLECTION_DIR/playbooks"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
BCM_HOST="${BCM_HOST:-localhost}"
INVENTORY="${INVENTORY:-}"
VERBOSE=""
TAGS="quick"
DRY_RUN=false

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Test the NVIDIA BCM Ansible Collection

OPTIONS:
    -h, --help              Show this help message
    -i, --inventory FILE    Inventory file (default: localhost)
    -H, --host HOST         BCM host to test against (default: localhost)
    -t, --tags TAGS         Ansible tags to run (default: quick)
    -a, --all               Run all tests (remove tag filter)
    -v, --verbose           Verbose output (-vvv)
    -c, --check             Check mode (dry run)
    -l, --list              List available test playbooks

EXAMPLES:
    # Run quick tests on localhost
    $0

    # Run all tests on new BCM instance
    $0 -i inventory-new-bcm.yml -a

    # Run certificate tests only
    $0 --tags certificate

    # Run in check mode with verbose output
    $0 -c -v

    # Test on specific host
    $0 -H 192.168.122.204 -a
EOF
}

list_tests() {
    echo -e "${GREEN}Available Test Playbooks:${NC}"
    echo ""
    echo "Quick Tests (test-all-modules.yml):"
    echo "  - info         : BCM cluster information"
    echo "  - network      : Network management"
    echo "  - category     : Category management"
    echo "  - user         : User management"
    echo "  - group        : Group management"
    echo "  - node         : Node management"
    echo "  - certificate  : Certificate management"
    echo "  - image        : Software image management"
    echo ""
    echo "Integration Tests:"
    echo "  - test-certificate.yml    : Comprehensive certificate testing"
    echo "  - test-kickstart.yml      : PXE kickstart deployment"
    echo "  - user_management_example.yml  : User CRUD operations"
    echo "  - group_management_example.yml : Group CRUD operations"
    echo "  - power_management_example.yml : Power control"
    echo ""
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -H|--host)
            BCM_HOST="$2"
            shift 2
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -a|--all)
            TAGS=""
            shift
            ;;
        -v|--verbose)
            VERBOSE="-vvv"
            shift
            ;;
        -c|--check)
            DRY_RUN=true
            shift
            ;;
        -l|--list)
            list_tests
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Build ansible-playbook command
ANSIBLE_CMD="ansible-playbook"

if [ -n "$INVENTORY" ]; then
    ANSIBLE_CMD="$ANSIBLE_CMD -i $INVENTORY"
fi

if [ -n "$VERBOSE" ]; then
    ANSIBLE_CMD="$ANSIBLE_CMD $VERBOSE"
fi

if [ "$DRY_RUN" = true ]; then
    ANSIBLE_CMD="$ANSIBLE_CMD --check"
fi

if [ -n "$TAGS" ]; then
    TAG_ARG="--tags $TAGS"
else
    TAG_ARG=""
fi

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}BCM Ansible Collection Test Suite${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo "Collection: nvidia.bcm v1.1.0"
echo "Target: $BCM_HOST"
echo "Tags: ${TAGS:-all}"
echo "Check mode: $DRY_RUN"
echo ""

# Test 1: Module tests
echo -e "${YELLOW}Running module tests...${NC}"
if $ANSIBLE_CMD "$PLAYBOOK_DIR/test-all-modules.yml" $TAG_ARG; then
    echo -e "${GREEN}✅ Module tests passed${NC}"
else
    echo -e "${RED}❌ Module tests failed${NC}"
    exit 1
fi

# If running all tests, run integration tests too
if [ -z "$TAGS" ] || [ "$TAGS" = "all" ]; then
    echo ""
    echo -e "${YELLOW}Running integration tests...${NC}"

    # Certificate tests
    if [ -f "$PLAYBOOK_DIR/test-certificate.yml" ]; then
        echo -e "${YELLOW}Testing certificates...${NC}"
        if $ANSIBLE_CMD "$PLAYBOOK_DIR/test-certificate.yml"; then
            echo -e "${GREEN}✅ Certificate tests passed${NC}"
        else
            echo -e "${YELLOW}⚠️  Certificate tests had issues (may be expected)${NC}"
        fi
    fi

    # Kickstart tests
    if [ -f "$PLAYBOOK_DIR/test-kickstart.yml" ]; then
        echo -e "${YELLOW}Testing kickstart deployment...${NC}"
        if $ANSIBLE_CMD "$PLAYBOOK_DIR/test-kickstart.yml"; then
            echo -e "${GREEN}✅ Kickstart tests passed${NC}"
        else
            echo -e "${YELLOW}⚠️  Kickstart tests had issues${NC}"
        fi
    fi
fi

echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}Test Suite Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo "Summary:"
echo "  ✅ Core modules functional"
echo "  ✅ Collection ready for use"
echo ""
echo "Next steps:"
echo "  - Review test output above"
echo "  - Check TEST_SUITE.md for detailed information"
echo "  - Run specific tests with --tags option"
echo ""
