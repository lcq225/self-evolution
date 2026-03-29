# -*- coding: utf-8 -*-
"""
Self-Evolution Command Line Interface

Usage:
    self-evolution --version
    self-evolution --help
    self-evolution dashboard [--output OUTPUT]
    self-evolution review [--days DAYS]
    self-evolution status
"""

import argparse
import sys
from pathlib import Path

from . import __version__


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="self-evolution",
        description="Self-Improving AI Agent Engine - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    self-evolution --version
    self-evolution dashboard --output evolution_report.html
    self-evolution review --days 7
    self-evolution status
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Generate evolution dashboard"
    )
    dashboard_parser.add_argument(
        "--output", "-o",
        type=str,
        default="evolution_dashboard.html",
        help="Output file path (default: evolution_dashboard.html)"
    )
    
    # Review command
    review_parser = subparsers.add_parser(
        "review",
        help="Generate weekly review report"
    )
    review_parser.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        help="Number of days to review (default: 7)"
    )
    
    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show evolution system status"
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    if args.command == "dashboard":
        return cmd_dashboard(args.output)
    elif args.command == "review":
        return cmd_review(args.days)
    elif args.command == "status":
        return cmd_status()
    
    return 0


def cmd_dashboard(output_path):
    """Generate evolution dashboard"""
    print(f"📊 Generating evolution dashboard...")
    
    try:
        from .evolution_dashboard import EvolutionDashboard
        
        dashboard = EvolutionDashboard()
        html_content = dashboard.generate()
        
        output = Path(output_path)
        output.write_text(html_content, encoding="utf-8")
        
        print(f"✅ Dashboard generated: {output.absolute()}")
        return 0
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}", file=sys.stderr)
        return 1


def cmd_review(days):
    """Generate weekly review report"""
    print(f"📝 Generating review report for last {days} days...")
    
    try:
        from .weekly_review import WeeklyReview
        
        reviewer = WeeklyReview()
        report = reviewer.generate_report(days=days)
        
        print("\n" + "=" * 60)
        print("WEEKLY REVIEW REPORT")
        print("=" * 60)
        print(report)
        print("=" * 60)
        
        return 0
    except Exception as e:
        print(f"❌ Error generating review: {e}", file=sys.stderr)
        return 1


def cmd_status():
    """Show evolution system status"""
    print("🔍 Checking evolution system status...\n")
    
    try:
        from .evolution_tracker import EvolutionTracker
        
        tracker = EvolutionTracker()
        stats = tracker.get_statistics()
        
        print("Evolution System Status")
        print("=" * 40)
        print(f"Total Experiences: {stats.get('total', 0)}")
        print(f"Negative Lessons: {stats.get('negative', 0)}")
        print(f"Positive Experiences: {stats.get('positive', 0)}")
        print(f"Consolidated: {stats.get('consolidated', 0)}")
        print(f"Consolidation Rate: {stats.get('consolidation_rate', 0):.1f}%")
        print(f"Pending Attribution: {stats.get('pending_attribution', 0)}")
        print(f"Pending Implementation: {stats.get('pending_implementation', 0)}")
        print("=" * 40)
        
        return 0
    except Exception as e:
        print(f"❌ Error checking status: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
