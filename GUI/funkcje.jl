module funkcje

using Plots
using Random

function environment(n::Int64, m::Int64)
    """
    funkcja tworząca środowisko wypełnione pakietami
    :param n:Int64: pierwszy wymiar srodowiska 
    :param m:Int64: drugi wymiar
    :return Environment:Array{Int64, 2}: środowisko
    """
    
    Environment = zeros(Int64, n, m)
    for i in 2:3:n
        Environment[i,:] = ones(Int64, 1, m)
    end
    return Environment
end

function golab_jastrzab(n_gol::Int64)
    """funkcja determinująca przeżycie gołębia w trakcie ucieczki - 50%
    :param n_gol:Int64: ilość gołębi przed spotkaniem
    :return n_gol:Int64: ilość gołębi po spotkaniu
    """
    if rand(0:1) == 0
        n_gol = n_gol - 1
    end
    return n_gol
end

function potyczki(n::Int64, m::Int64, macierz::Array{Int64,2}, g::Int64, ja::Int64)
    """funkcja determinująca stan populacji po wylosowaniu miejsc przy pakietach żywnościowych
    :param n: wymiar środowiska 
    :param m: wymiar środowiska
    :param macierz: macierz środowiska
    :param g: ilość gołębi przed potyczkami
    :param ja: ilość jastrzębi przed potyczkami
    :return g: ilość gołębi po potyczkach
    :return ja: ilość jastrzębi po potyczkach
    """
    for i in 2:3:n, j in 1:m    
        suma = macierz[i-1,j] + macierz[i+1,j]
        if suma == 11
            g = golab_jastrzab(g)
            ja = ja + 1
        elseif suma == 6
            g = g
        elseif suma == 16 
            ja = ja - 2
        elseif suma == 3
            g += 2
        elseif suma == 8
            j += 2
        end 
    return g,ja
    end
end

function potyczkiii(n, m, macierz, g, ja)
    """funkcja determinująca stan populacji po wylosowaniu miejsc przy pakietach żywnościowych
    :param n: wymiar środowiska 
    :param m: wymiar środowiska
    :param macierz: macierz środowiska
    :param g: ilość gołębi przed potyczkami
    :param ja: ilość jastrzębi przed potyczkami
    :return g: ilość gołębi po potyczkach
    :return ja: ilość jastrzębi po potyczkach
    """
    
    for i in 2:3:n, j in 1:m    
        suma = macierz[i-1,j] + macierz[i+1,j]
        if macierz[i,j] == 1
            if suma == 11
                g = golab_jastrzab(g)
                ja = ja + 1
            elseif suma == 6
                g = g
            elseif suma == 16 
                ja = ja - 2
            elseif suma == 3
                g += 2
            elseif suma == 8
                ja += 2
            end 
            
        elseif macierz[i,j] == 0
            if suma == 11
                g = g - 1
            elseif suma == 6
                g = g - 2
            elseif suma == 16 
                ja = ja - 2
            elseif suma == 3
                g -= 1
            elseif suma == 8
                ja -= 1
            end
        end
    return g,ja
    end
end

function golabki(macierz::Array, ngol::Int64)
    """funkcja generująca rozstawienie gołębi w środowisku
    :param macierz: macierz środowiska
    :param ngol: ilość gołębi
    """

    if ngol != 0  
        for i in 1:1:ngol
            z = findall(x -> x ==0, macierz)
            macierz[rand(z)] = 3
        end
    end
    return macierz
end

function jastrzabki(macierz::Array, njas::Int64)
    """funkcja generująca rozstawienie jastrzębi w środowisku
    :param macierz: macierz środowiska
    :param ngol: ilość jastrzębi
    """
    if njas != 0
        for i in 1:1:njas
            z = findall(x -> x ==0, macierz)
            macierz[rand(z)] = 8
        end
    end
    return macierz
end

function check(n::Int64, m::Int64, ng::Int64, nja::Int64)
    """funkcja sprawdzająca nadmiar populacji i ilość ptaków wysłaną na wygnanie
    :param n: wymiar środowiska 
    :param m: wymiar środowiska
    :param ng: ilość gołębi
    :param nja: ilość jastrzębi
    :return ng: ilość gołębi w normalnym środowisku
    :return nja: ilość jastrzębi w normalnym środowisku
    :return fight_g: ilość gołębi na wygnaniu
    :return fight_ja: ilość jastrzębi na wygnaniu
    """
    if ng + nja > 2*n*m/3
        env_ng = Int64(round(ng/(ng+nja) * 2*n*m/3))
        env_ja = Int64(round(nja/(ng+nja) * 2*n*m/3))
        fight_g = ng - env_ng
        fight_ja = nja - env_ja
        ng = env_ng
        nja = env_ja
        return ng, nja, fight_g, fight_ja
    else
        fight_g = 0
        fight_ja = 0
        return ng, nja, fight_g, fight_ja
    end
end

function fight_club(n_gol::Int64, n_jas::Int64)
    """funkcja determinująca sytuację na wygnaniu, tworząca macierz środowiska
    :param n_gol: liczba gołębi przed walką
    :param n_gol: liczba jastrzębi przed walką
    :return M: macierz środowiska
    """
    if (n_gol + n_jas)%2 == 0
        n = Int64((n_gol + n_jas)/2)
        M = zeros(Int64, 2, n)
        if n_gol != 0
            golabki(M, n_gol)
        end
        if n_jas!=0
            jastrzabki(M, n_jas)
        end
    else
        n = Int64((n_gol + n_jas + 1)/2) 
        M = zeros(Int64, 2, n)
        if n_gol != 0
            golabki(M, n_gol)
        end
        if n_jas!=0
            jastrzabki(M, n_jas)
        end
    end
    return M
end
     
function fight(macierz::Array, n_gol::Int64, n_jas::Int64)
    """funkcja determinująca sytuację na wygnaniu, tworząca macierz środowiska
    :param macierz: macierz środowiska na wygnaniu
    :param n_gol: liczba gołębi przed walką
    :param n_gol: liczba jastrzębi przed walką
    :return n_gol: liczba gołębi po walce
    :return n_jas: liczba jastrzębi po walce
    """
    for i in 1:size(macierz)[2]
        suma = macierz[1,i] + macierz[2,i]
        if suma == 6
            n_gol -= 1
        elseif suma == 16
            n_jas -= 1
        elseif suma == 11
            if rand(0:1) == 0
                n_gol -= 1
            else
                n_jas -= 1
            end
        end
    end
    return n_gol, n_jas
end

function environment_food_amount(size1 = 21, size2 = 21, amount = 100)
    """funkcja generująca środowiska z mniejszą ilościa pakietów
    :param size1:Int64: wymiar środowiska
    :param size2:Int64: wymiar środowiska
    :param amount:Int64: ilość pakietów
    :return Environment: środowisko
    """
#ilość wieszy musi być podzielna przez 3
    if size1 % 3 != 0
        throw(DomainError(size, "incorrect size"))
    end
    Environment = zeros(Int64, size1, size2)
    A = zeros(Int64, 1, size2*(fld(size1-2,3)+1))
    A[1,1:amount] = ones(Int64, 1, amount)
    A = Random.shuffle(A)
    k = 1
    for i in 2:3:size1
        Environment[i,:] = A[1, k:(k+size1-1)]
        k += size1
    end
    return Environment
end

function action(n::Int64, m::Int64, n_gol::Int64, n_jas::Int64, p::Int64, A, pack = 1, index = 1) ##pack to opcjonalna liczba pakietów
    """główna funkcja generująca statystyki populacji
    :param n: wymiar środowiska 
    :param m: wymiar środowiska
    :param n_gol: ilość gołębi
    :param n_jas: ilość jastrzębi
    :param p: ilość wykonań funkcji (ilość dni)
    :param A: macierz startowa, o pierwszym wymiarze identycznym z param p
    :param pack: ilość pakietów, domyślnie jest to maksymalna ilość
    :param index: indeks służący do generowania wykresów
    :return A: środowisko końcowe, gdy skończył się zakres p
    """
    
    if p == 0
        return A
    end
   
    if pack == 1 # czyli max pakietów, brak nieurodzaju
        srod = environment(n,m) ##mamy pakiety
    else
        if pack < 1/3*n*m
            srod = environment_food_amount(n,m,pack)
        else
            pack = 1
            srod = environment(n,m)
        end
    end
    #print(srod)
    a = check(n, m, n_gol, n_jas) #sprawdzamy czy nie ma za dużo ptaszków, zwraca jako (gol_safe, jas_safe, gol_fight, jas_fight)
    n_gol = a[1]
    n_jas = a[2]

    golabki(srod, n_gol)
    jastrzabki(srod, n_jas)  ##mamy srodowisko z ptaszkami
    
    result = potyczkiii(n,m,srod, n_gol, n_jas) ##mamy stan populacji po potyczkach
    n_gol = result[1] ##liczba gołębi
    n_jas = result[2]
    
    ##w miedzyczasie fight club :
    
    
    b = fight(fight_club(a[3],a[4]), a[3], a[4]) #populacja po fight clubie - (gol, jas)
    
    n_gol += b[1] ##ostateczna ilosc golebi - ta bezpieczna + fight club
    n_jas += b[2] ## -||- jastrzebi
    gol_fight = b[1] ##ilość ptakow po fightcie, może się przyda c:
    jas_fight = b[2]
    
    A[index, 1] = n_gol
    A[index, 2] = n_jas
    index += 1
    #println(n_gol,",", n_jas,",", gol_fight, ",",jas_fight)
    
    action(n, m, n_gol, n_jas, p-1, A, pack, index) #i lecimy rekurencją
end
end