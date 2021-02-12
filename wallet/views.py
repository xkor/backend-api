from rest_framework import views, response, validators
from .models import Wallet, WalletTransaction
from .serializers import WalletSerializer, CreateTransactionSerializer, WalletTransactionSerializer


class WalletView(views.APIView):
    def get(self, request, wallet_id):
        try:
            instance = Wallet.objects.get(wallet_id=wallet_id)
            serializer = WalletSerializer(instance)
            return response.Response(serializer.data)
        except Wallet.DoesNotExist:
            raise validators.ValidationError({'message': 'Bunday wallet id mavjud emas'})


class TransactionView(views.APIView):
    def post(self, request):
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(vars(serializer))
        from_wallet = Wallet.objects.get(wallet_id=serializer.data.get('from_wallet_id'))
        to_wallet = Wallet.objects.get(wallet_id=serializer.data.get('to_wallet_id'))

        from_wallet.balance -= serializer.data.get('amount')
        to_wallet.balance += serializer.data.get('amount')

        try:
            from_wallet.save()
            to_wallet.save()
        except Exception as e:
            raise validators.ValidationError({'message': 'puliz yetmadi'})
        wt_transaction = WalletTransaction.objects.create(
            from_wallet=from_wallet,
            to_wallet=to_wallet,
            amount=serializer.data.get('amount')
        )
        transaction_serializer = WalletTransactionSerializer(wt_transaction)

        return response.Response(transaction_serializer.data)


# {'from_wallet_id': '8600404050506060', 'to_wallet_id': '8600202010103030 ', 'amount': 5000}
