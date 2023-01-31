# contract
Creates a pdf contract (rus)
## INSTALL
```
pip3 install -r requirements.txt

# Copy examples
cp examples/config.py contract/
cp examples/template.html ./

# Edit contract/config.py file to replace APARTMENTS 
#        and REQUIRED_VALUES with your data.
```

## USAGE
```
from contract import config, Contract
contract = Contract(config.REQUIRED_VALUES)
contract.write_pdf('out.pdf')
```
