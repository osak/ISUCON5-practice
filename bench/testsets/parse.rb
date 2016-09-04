require 'json'

json = JSON.parse(File.read('testsets.json'))
json.each_with_index do |testset, i|
  File.open("testset#{i}.json", "w") do |f|
    f.puts(testset.to_json)
  end
end
