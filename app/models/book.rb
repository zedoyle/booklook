class Book < ActiveRecord::Base

  def versions
    bid = self.id
    match = Version.where("book_id = ?", bid)
    return match
  end

end
