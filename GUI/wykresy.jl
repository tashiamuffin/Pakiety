include("C:\\Users\\mazur\\OneDrive\\Pulpit\\pakiety prezentacja\\funkcje.jl") #sciezka do funkcji
using .funkcje

function converting(n, m, n_gol, n_jas, p, pack = 1, index = 1)
    text = "["
    A = zeros(Int64, p, 2)
    charts = funkcje.action(n, m, n_gol, n_jas, p, A, pack, index)
    for i in 1:2
        text *= "["
        for j in 1:size(charts)[1]
            if j == 1
                text *= string(charts[j,i])
            else
                text *= ", "
                text *= string(charts[j,i])
            end
        end
        text *= "]"
    end
    text *= "]"
return text
end