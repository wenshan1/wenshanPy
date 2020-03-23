'''
Created on Apr 14, 2018

@author: wenshan
'''

from elftools.elf.elffile import ELFFile 
from elftools.elf.sections import SymbolTableSection

def process_file(filename):
    print('Processing file:', filename)
     
    with open (filename, 'rb') as f:
        elffile = ELFFile (f)
        section = elffile.get_section_by_name('.dynsym')
        if not section:
            print('  No symbol table found. Perhaps this ELF has been stripped?')
            return
        # A section type is in its header, but the name was decoded and placed in
        # a public attribute.
        print('  Section name: %s, type: %s' %(
              section.name, section['sh_type']))
        
        if isinstance(section, SymbolTableSection):
            num_symbols = section.num_symbols()
            print("  It's a symbol section with %s symbols" % num_symbols)
            print("  The name of the last symbol in the section is: %s" % (
                  section.get_symbol(num_symbols - 1).name))
            
            print(section.get_symbol(num_symbols - 1).entry )
         

if __name__ == '__main__':
    process_file ("/bin/ls");