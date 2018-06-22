import grpc

import pi_pb2
import pi_pb2_grpc


def main():
    channel = grpc.insecure_channel('127.0.0.1:8080')
    client = pi_pb2_grpc.PiCalculatorStub(channel)

    for i in range(1000):
        print("pi(%d) =" % i, client.Calc(pi_pb2.PiRequest(n=i)).value)


if __name__ == '__main__':
    main()
