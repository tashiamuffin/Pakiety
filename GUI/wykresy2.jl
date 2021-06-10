include("C:\\Users\\mazur\\OneDrive\\Pulpit\\pakiety prezentacja\\funkcje2.jl") #sciezka do funkcji2
using .funkcje2

function converting(n, m, n_gol, n_jas, ch_g, ch_j, p, deadliness, pack = 1, index = 1)
    text = "["
    A = zeros(Int64, p, 2)
    charts = funkcje2.action2(n, m, n_gol, n_jas, ch_g, ch_j, p, deadliness, A, index)
    for i in 1:4
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