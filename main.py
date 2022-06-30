import concatnation
import scanner
import normalization
import datesEdit
# runs all the files one after the other to complete the data
if __name__ == '__main__':
    scanner.main()
    normalization.normalization_main()
    datesEdit.dates_edit_main()
    concatnation.concatanation_main()