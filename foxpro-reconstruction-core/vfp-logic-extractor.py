# ============================================================================
# 🦊 QCA Genesis AI Studio | The Relic Breaker
# File: vfp-logic-extractor.py
# Entity: The Carbon-Dater (Visual FoxPro Analyzer)
# Purpose: Static AST-like parsing of legacy .prg and .scx FoxPro files.
#          Extracts raw business logic before AI transmutation.
# Architect: Pavlo Radkoff (QCA)
# ============================================================================

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [QCA-VFP-EXTRACTOR] - %(levelname)s - %(message)s')

class VisualFoxProArchaeologist:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.logic_graph: Dict[str, dict] = {}
        
        # QCA Regex Arsenal for VFP Syntax
        self.proc_pattern = re.compile(r'^\s*(PROCEDURE|FUNCTION)\s+([a-zA-Z0-9_]+)', re.IGNORECASE)
        self.endproc_pattern = re.compile(r'^\s*(ENDPROC|ENDFUNC)', re.IGNORECASE)
        self.sql_pattern = re.compile(r'^\s*SELECT\s+.*FROM\s+', re.IGNORECASE)

    def exhume_file(self, file_path: Path) -> None:
        """Parses a single .prg file to extract isolated logic blocks."""
        logging.info(f"Initiating extraction sequence on relic: {file_path.name}")
        
        current_block: Optional[str] = None
        block_content: List[str] = []
        sql_queries: int = 0

        with open(file_path, 'r', encoding='latin-1', errors='ignore') as relic_file:
            for line_number, line in enumerate(relic_file, 1):
                proc_match = self.proc_pattern.match(line)
                
                if proc_match:
                    current_block = proc_match.group(2).upper()
                    block_content = []
                    continue
                
                if self.endproc_pattern.match(line) and current_block:
                    # Finalize block extraction
                    self.logic_graph[current_block] = {
                        "source_file": file_path.name,
                        "lines_of_code": len(block_content),
                        "sql_operations_detected": sql_queries,
                        "raw_payload": "\n".join(block_content)
                    }
                    current_block = None
                    sql_queries = 0
                    continue

                if current_block:
                    block_content.append(line.strip())
                    if self.sql_pattern.search(line):
                        sql_queries += 1

    def generate_transmutation_matrix(self, output_file: str = "vfp_ast_matrix.json") -> None:
        """Exports the extracted logic graph for the AI Workers pipeline."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.logic_graph, f, indent=4)
        logging.info(f"Transmutation matrix forged successfully: {output_file}. Ready for AI injection.")

if __name__ == "__main__":
    # Example execution sequence (QCA Lab usage)
    archaeologist = VisualFoxProArchaeologist(target_dir="./legacy_source")
    # archaeologist.exhume_file(Path("./legacy_source/main_payroll.prg"))
    # archaeologist.generate_transmutation_matrix()
    logging.info("VFP Archaeologist module initialized and awaiting commands.")