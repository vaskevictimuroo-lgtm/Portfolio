import numpy as np
num1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num4 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num5 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num6 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num7 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num8 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num9 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

num9_with_error = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 1, 0, 0, 0, 0, 1, 0],
                            [0, 1, 1, 1, 0, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])

num0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 1, 0, 0, 0, 1, 1, 0],
                 [0, 1, 0, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

filename = "trained_weights.npz"

epoch = [num.flatten() for num in [num0, num1, num2, num3, num4, num5, num6, num7, num8, num9]]
hint = np.eye(10)

input_size = 8*8
hidden_size = 1000
output_size = 10

normalize1 = np.sqrt(6/(hidden_size+input_size))
normalize2 = np.sqrt(6/(hidden_size+output_size))

w1 = np.random.randn(hidden_size, input_size) * normalize1
b1 = np.zeros((hidden_size, 1))
w2 = np.random.randn(output_size, hidden_size) * normalize2
b2 = np.zeros((output_size, 1))



def tanh(x):
    return np.tanh(x)

def dxtanh(x):
    return 1 - np.tanh(x) ** 2

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

def forward(x):
    res1 = tanh(np.dot(w1, x) + b1.flatten())
    res2 = softmax(np.dot(w2, res1) + b2.flatten())
    return res2

def forward_train(x):
    z1 = np.dot(w1, x) + b1.flatten()
    a1 = tanh(z1)
    z2 = np.dot(w2, a1) + b2.flatten()
    y_pred = softmax(z2)
    return y_pred, z1, a1

def load_weights():
    global w1, w2, b1, b2
    data = np.load(filename)
    w1, w2, b1, b2 = data['w1'], data['w2'], data['b1'], data['b2']
    print(f"Веса загружены из {filename}")

def save_weights():
    np.savez(filename, w1=w1, w2=w2, b1=b1, b2=b2)
    print(f"Веса сохранены в {filename}")

def BackPropagation(learning_rate=0.0001, epoch_amount=100000):
    global w1, w2, b1, b2, filename
    load_weights()
    for epoch_num in range(epoch_amount):
        for i in range(len(epoch)):
            x = epoch[i]
            y_pred, z1, a1 = forward_train(x)
            y_true = hint[i]
            
            error_output = y_pred - y_true
            grad_w2 = np.outer(error_output, a1)
            error_hidden = np.dot(w2.T, error_output).reshape(-1, 1) * dxtanh(z1).reshape(-1, 1)
            grad_w1 = np.outer(error_hidden.flatten(), x)
            grad_b2 = error_output.reshape(-1, 1)
            grad_b1 = error_hidden.reshape(-1, 1)
            
            w1 -= learning_rate * grad_w1
            w2 -= learning_rate * grad_w2
            b1 -= learning_rate * grad_b1
            b2 -= learning_rate * grad_b2
        
        if epoch_num % 1000 == 0:
            print(f"Эпоха {epoch_num} завершена")
    print(f"Эпоха {epoch_amount} завершена")
    print("Обучение завершено")
    save_weights()

def test_work():
    for i in range(10):
        test_number = epoch[i]
        y_pred = forward(test_number)
        predicted = np.argmax(y_pred)
        confidence = y_pred[predicted] * 100
        print(f"Цифра {i}: предсказано {predicted} (уверенность: {confidence:.2f}%)")

if __name__ == "__main__":
    try:
        load_weights()
    except:
        print("Обученные веса не найдены, начинаем обучение...")
        BackPropagation(epoch_amount=10000)
        save_weights()

    test_work()
    test_number = num9_with_error.flatten()
    y_pred = forward(test_number)
    predicted = np.argmax(y_pred)
    confidence = y_pred[predicted] * 100
    print(f"Цифра 9 с ошибкой: предсказано {predicted} (уверенность: {confidence:.2f}%)")


