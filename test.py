from scipy import optimize

def f(x):
    return (x-2)**2+(x-3)**2+(x-4)**2

# optimize in centrailized way
# the args is the parameter passed to function f, you can refer to official scipy.optimize api doc for more details

# def f(x,a):
#     return (x-a)**2

def lagrange1(x,a,b):
    return (x-2)**2 + a*(x - b) + 0.5*(x-b)**2

def lagrange2(x,a,b):
    return (x-3)**2 + a*(x - b) + 0.5*(x-b)**2

def lagrange3(x,a,b):
    return (x-4)**2 + a*(x - b) + 0.5*(x-b)**2

# optimize in distributed way
# node1: (x-2)**2
# node2: (x-3)**2

def lag1(x,a,b):
    return (x-2)**2+x*a+0.5*(x-b)**2

def lag2(x,a,b,c):
    return (x-3)**2+x*a+0.5*(x-b)**2+0.5*(x-c)**2

def lag3(x,a,b):
    return (x-4)**2+x*a+0.5*(x-b)**2

def l1(x,a):
    return (x-2)**2+x*a+(x)**2

def l2(x,a):
    return (x-3)**2+x*a+2*(x)**2

def l3(x,a):
    return (x-4)**2+x*a+(x)**2

if __name__ == '__main__':

    # original problem: minimize (x-2)**2+(x-3)**2+(x-4)**2

    # in centralized way:
    # x = 0
    # print("before optimization : %f"%x)
    # x = optimize.fmin_cg(f,[x])
    # print("centralized result : %f"%x)

    # in centralized ADMM:
    # dual variable

    # x1 = 1
    # x2 = 1
    # x3 = 1

    # y1 = 0
    # y2 = 0
    # y3 = 0

    # z = 0


    # # fix the number of iterations temporarily
    # for i in range(10):
    #     # update xi
    #     # for node 1
    #     x1 = optimize.fmin_cg(lagrange1,[x1],args=(y1,z))

    #     # for node 2:
    #     x2 = optimize.fmin_cg(lagrange2,[x2],args=(y2,z))

    #     # for node 3:
    #     x3 = optimize.fmin_cg(lagrange3,[x3],args=(y3,z))


    #     # update z
    #     z = (x1+x2+x3)/3

    #     # update yi(dual variable):
    #     # for node 1:
    #     y1 = y1 + (x1 - z)
    #     # for node 2:
    #     y2 = y2 + (x2 - z)
    #     # for node 3:
    #     y3 = y3 + (x3 - z)

    # print("x1 = %f"%x1)
    # print("x2 = %f"%x2)
    # print("x3 = %f"%x3)

    # in decentralized ADMM:
    # using the following graph:
    # 1 -- 2 -- 3

    # x1 = 0
    # x2 = 0
    # x3 = 0

    # x1_ = 0
    # x2_ = 0
    # x3_ = 0

    # y12 = 0
    # y23 = 0

    # for i in range(30):
    #     # for node1:
    #     x1 = optimize.fmin_cg(lag1,[x1],args=(y12,0.5*(x1_+x2_)))

    #     # for node2:
    #     x2 = optimize.fmin_cg(lag2,[x2],args=((-y12+y23),0.5*(x1_+x2_),0.5*(x2_+x3_)))

    #     # for node3:
    #     x3 = optimize.fmin_cg(lag3,[x3],args=(-y23,0.5*(x2_+x3_)))

    #     # for dual variable
    #     y12 = y12 + 0.5*(x1 - x2)
    #     y23 = y23 + 0.5*(x2 - x3)

    #     x1_ = x1
    #     x2_ = x2
    #     x3_ = x3


    # print("decentralized ADMM x1 = %f"%x1)
    # print("decentralized ADMM x2 = %f"%x2)
    # print("decentralized ADMM x3 = %f"%x3)

# --------------------------------
# use the formulation in paper
    x1 = 0.0
    x2 = 0.0
    x3 = 0.0

    x1_ = 0.0
    x2_ = 0.0
    x3_ = 0.0

    y12 = 0.0
    y23 = 0.0

    for i in range(30):
        # for node1:
        x1 = optimize.fmin_cg(l1,[x1],args=(y12-x1_-x2_,))

        # for node2:
        x2 = optimize.fmin_cg(l2,[x2],args=((-y12+y23)-(x1_+x2_)-(x2_+x3_),))

        # for node3:
        x3 = optimize.fmin_cg(l3,[x3],args=(-y23-(x2_+x3_),))

        # for dual variable
        y12 = y12 + (x1 - x2)
        y23 = y23 + (x2 - x3)

        x1_ = x1
        x2_ = x2
        x3_ = x3


    print("decentralized ADMM x1 = %f"%x1)
    print("decentralized ADMM x2 = %f"%x2)
    print("decentralized ADMM x3 = %f"%x3)



