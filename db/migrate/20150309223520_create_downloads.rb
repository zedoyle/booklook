class CreateDownloads < ActiveRecord::Migration
  def change
    create_table :downloads do |t|
      t.datetime :when
      t.references :user, index: true
      t.references :link, index: true

      t.timestamps null: false
    end
    add_foreign_key :downloads, :users
    add_foreign_key :downloads, :links
  end
end
