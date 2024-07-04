import eth_abi
import eth_abi.abi
from eth_account.messages import encode_defunct
import web3
import pydash as py_

from config import Config


class SignatureHelper:

    @staticmethod
    def generate_bridge_signature(data):
        '''
        '''

        from_chain_id = py_.get(data, "from_chain_id")
        to_chain_id = py_.get(data, 'to_chain_id')
        user_address = py_.get(data, 'user_address')
        contract_address = py_.get(data, 'contract_address')

        if to_chain_id == int(Config.BNB_CHAIN_ID):
            contract_address = Config.BNB_CONTRACT_ADDRESS
        else:
            if to_chain_id == int(Config.ETH_CHAIN_ID):
                contract_address = Config.ETH_CONTRACT_ADDRESS

        tx_hash = py_.get(data, 'tx_hash')
        amount = py_.get(data, 'amount')

        _web3 = web3.Web3()

        encoded_message = eth_abi.abi.encode(
            [
                'uint256',  # to_chain_id
                'uint256', # from_chain_id
                'address',  # user_address
                'address',  # contract creator
                'string',  # tx_hash
                'uint256',  # amount
            ],
            [
                to_chain_id,
                from_chain_id,
                user_address,
                contract_address,
                tx_hash,
                int(amount),
            ]
        )

        message = encode_defunct(web3.Web3.keccak(encoded_message))
        _signed_message = _web3.eth.account.sign_message(
            message,
            private_key=py_.get(data, 'signature_sign_pk')
        )

        return _signed_message.signature.hex()
